import { useState, useEffect } from "react";
import api from "../../../api";
import { checkInternetConnection, getResponseMessages } from "../../../utils";
import style from "../../../styles/resetpasswordscreen.module.css";

function ResetPassword({ route }) {
  const [email, setEmail] = useState("");
  const [response, setResponse] = useState(null);
  const [visible, setVisible] = useState(false);

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
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      const message =
        "Network issue detected. Please ensure you are connected to the internet and try again.";

      setResponse({ message: message, type: "error", id: Date.now() });
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
            "Too many requests were made. Please try again after sometime.",
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
    }
  };

  return (
    <div className={style.resetPasswordPage}>
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
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                />
              </div>
              <div className={style.buttonContainer}>
                <button type="submit" onClick={handleSubmit}>
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        className={`${style.notificationContainer} ${
          visible ? style.show : ""
        } ${response?.type === "error" ? style.error : ""}`}
      >
        {response?.message}
      </div>
    </div>
  );
}

export default ResetPassword;
