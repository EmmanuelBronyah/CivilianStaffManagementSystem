import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import checkInternetConnection from "../utils/checkInternetConnection";
import getResponseMessages from "../utils/extractResponseMessage";
import style from "../styles/pages/confirmpasswordscreen.module.css";
import Notification from "../Components/NotificationComponent";
import ClipLoader from "react-spinners/ClipLoader";

function ConfirmPasswordReset({ route }) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [response, setResponse] = useState(null);
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { uid, token } = useParams();

  useEffect(() => {
    if (response?.message) {
      setVisible(true);
    }

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      setLoading(false);
      const message =
        "Network issue detected - Please ensure you are connected to the internet and try again";

      setResponse({ message: message, type: "error", id: Date.now() });
      return;
    }

    if (!password || !confirmPassword) {
      setLoading(false);
      setResponse({
        message: "Password fields cannot be blank",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      const res = await api.post(route, {
        uid: uid,
        token: token,
        new_password1: password,
        new_password2: confirmPassword,
      });
      if (res.status === 200) {
        const message = getResponseMessages(res);
        setResponse({ message: message, id: Date.now() });

        setTimeout(() => {
          navigate("/auth/login");
        }, 3000);
      }
    } catch (error) {
      const errorObj = error.response;

      if (errorObj) {
        const message = getResponseMessages(errorObj);
        setResponse({ message: message, type: "error", id: Date.now() });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={style.confirmPasswordPage}>
      {/* CONFIRM PASSWORD FORM SECTION */}
      <div className={style.wrapper}>
        <div className={style.logoTextAndConfirmPasswordContainer}>
          <div className={style.logoText}>CiviBase</div>
          <div className={style.confirmPasswordContainer}>
            <div className={style.inputBoxAndButton}>
              <div>
                <input
                  type="password"
                  value={password}
                  disabled={loading}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="New Password"
                />
              </div>
              <div>
                <input
                  type="password"
                  value={confirmPassword}
                  disabled={loading}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm Password"
                />
              </div>
              <div className={style.buttonContainer}>
                <button type="submit" onClick={handleSubmit}>
                  {loading ? <ClipLoader size={13} color="#fff" /> : "Submit"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Notification Component */}
      <Notification isVisible={visible} response={response} />
    </div>
  );
}

export default ConfirmPasswordReset;
