import { useState, useEffect } from "react";
import api from "../api";
import checkInternetConnection from "../utils/checkInternetConnection";
import getResponseMessages from "../utils/extractResponseMessage";
import style from "../styles/pages/resetpasswordscreen.module.css";
import Notification from "../Components/NotificationComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { useTheme } from "../context/ThemeContext";
import ThemeToggle from "../Components/ThemeToggleComponent";

function ResetPassword({ route }) {
  const [email, setEmail] = useState("");
  const [response, setResponse] = useState(null);
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const { theme, setTheme } = useTheme();

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

    if (!email) {
      setLoading(false);
      setResponse({
        message: "Enter email address",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      const res = await api.post(route, { email: email });

      if (res.status === 200) {
        const message = getResponseMessages(res);
        setResponse({ message: message, id: Date.now() });
      }
    } catch (error) {
      if (error.response.status === 429) {
        setResponse({
          message:
            "Too many requests were made - Please try again after sometime",
          type: "error",
          id: Date.now(),
        });
      } else {
        const errorObj = error.response;

        if (errorObj) {
          const message = getResponseMessages(errorObj);
          setResponse({ message: message, type: "error", id: Date.now() });
        }
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`${style.resetPasswordPage} ${!theme && style.dark}`}>
      <ThemeToggle className={style.switch} />
      {/* RESET PASSWORD FORM SECTION */}
      <div className={style.wrapper}>
        <div className={style.logoTextAndResetPasswordContainer}>
          <div className={style.logoText}>CiviBase</div>
          <div className={style.resetPasswordContainer}>
            <div className={style.inputBoxAndButton}>
              <div>
                <input
                  type="email"
                  value={email}
                  disabled={loading}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                />
              </div>
              <div className={style.buttonContainer}>
                <button type="submit" onClick={handleSubmit}>
                  {loading ? <ClipLoader size={13} color="#fff" /> : "Verify"}
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

export default ResetPassword;
