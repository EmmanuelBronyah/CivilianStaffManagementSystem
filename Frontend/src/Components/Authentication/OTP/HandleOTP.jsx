import { useState, useEffect } from "react";
import api from "../../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../../../constants";
import { useNavigate } from "react-router-dom";
import { checkInternetConnection } from "../../../utils";
import style from "../../../styles/otpscreen.module.css";
import getResponseMessages from "../Login/utils";

function ResendAndVerifyOTP({ route }) {
  const [otp, setOTP] = useState("");
  const [response, setResponse] = useState(null);
  const [visible, setVisible] = useState(false);
  const navigate = useNavigate();

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
    if (e) e.preventDefault();
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tokenData = { tokens: { temp_token: temp_token, otp_token: otp } };
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      const message =
        "Network issue detected. Please ensure you are connected to the internet and try again.";

      setResponse({ message: message, type: "error", id: Date.now() });
      return;
    }

    try {
      const res = await api.post(route, tokenData);
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        localStorage.removeItem(TEMP_TOKEN);

        setResponse({ message: "Login successful", id: Date.now() });

        setTimeout(() => {
          navigate("/dashboard");
        }, 3000);
      }
    } catch (error) {
      const errorObj = error.response;
      if (errorObj) {
        const message = getResponseMessages(errorObj);
        setResponse({ message: message, type: "error", id: Date.now() });
      }
    }
  };

  const handleResend = async (e) => {
    e.preventDefault();
    const otpResendRoute = "api/resend-otp/";
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tempTokenData = { tokens: { temp_token: temp_token } };
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      const message =
        "Network issue detected. Please ensure you are connected to the internet and try again.";

      setResponse({ message: message, type: "error", id: Date.now() });
      return;
    }

    try {
      const res = await api.post(otpResendRoute, tempTokenData);
      if (res.status === 200) {
        const tempToken = res.data.temp_token;
        localStorage.setItem(TEMP_TOKEN, tempToken);

        const message = getResponseMessages(response);
        setResponse({ message: message, id: Date.now() });
      }
    } catch (error) {
      const errorObj = error.response;
      if (errorObj) {
        const message = getResponseMessages(errorObj);
        setResponse({ message: message, type: "error", id: Date.now() });
      }
    }
  };

  return (
    <div className={style.otpPage}>
      {/* OTP FORM SECTION */}
      <div className={style.wrapper}>
        <div className={style.logoTextAndOtpContainer}>
          <div className={style.logoText}>CiviBase</div>
          <div className={style.otpContainer}>
            <div className={style.inputBoxesAndButtons}>
              <div>
                <input
                  type="text"
                  value={otp}
                  onChange={(e) => setOTP(e.target.value)}
                  placeholder="Enter 6-digit code"
                />
              </div>
              <div className={style.buttonsContainer}>
                <button type="submit" onClick={handleSubmit}>
                  Verify
                </button>
                <button type="submit" onClick={handleResend}>
                  Resend
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

export default ResendAndVerifyOTP;
