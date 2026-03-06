import { useState, useEffect } from "react";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../constants";
import { useNavigate } from "react-router-dom";
import checkInternetConnection from "../utils/checkInternetConnection";
import getResponseMessages from "../utils/extractResponseMessage";
import style from "../styles/pages/otpscreen.module.css";
import Notification from "../Components/NotificationComponent";
import ClipLoader from "react-spinners/ClipLoader";
import OTPTimer from "../Components/OTPTimerComponent";
import handleRevokeAndResendOTP from "../utils/revokeAndResendOtp";

function ResendAndVerifyOTP({ route }) {
  const [otp, setOTP] = useState("");
  const [response, setResponse] = useState(null);
  const [verifyLoading, setVerifyIsLoading] = useState(false);
  const [resendLoading, setResendIsLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const [isExpired, setIsExpired] = useState(false);
  const [expiryTimestamp, setExpiryTimestamp] = useState(null);
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

  useEffect(() => {
    const storedExpiry = localStorage.getItem("otp_expiry");

    if (storedExpiry) {
      setExpiryTimestamp(Number(storedExpiry));
    } else {
      const expiry = Date.now() + 5 * 60 * 1000;
      localStorage.setItem("otp_expiry", expiry);
      setExpiryTimestamp(expiry);
    }
  }, []);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setVerifyIsLoading(true);

    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tokenData = { tokens: { temp_token: temp_token, otp_token: otp } };
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      setVerifyIsLoading(false);
      setResponse({
        message: "Network issue detected. Please ensure you are connected.",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    if (!otp) {
      setVerifyIsLoading(false);
      setResponse({
        message: "Enter 6 digit code",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      const res = await api.post(route, tokenData);
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);

        setResponse({
          message: "Login successful. Redirecting...",
          id: Date.now(),
        });

        setTimeout(() => {
          navigate("/dashboard");
        }, 4000);
      }
    } catch (error) {
      const errorObj = error.response;
      if (errorObj) {
        const message = getResponseMessages(errorObj);
        setResponse({ message: message, type: "error", id: Date.now() });
      }
    } finally {
      setVerifyIsLoading(false);
    }
  };

  const handleResend = async (e) => {
    e.preventDefault();
    setResendIsLoading(true);

    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      setResendIsLoading(false);
      setResponse({
        message: "Network issue detected. Please ensure you are connected.",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      console.log("ABOUT TO RUN <handleRevokeAndResendOTP> in OTPPage.jsx");

      // Handle revoking previous OTP's and Re-sending a new OTP
      await handleRevokeAndResendOTP(setResponse, setResendIsLoading);
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
            <div className={style.inputContainer}>
              <input
                type="text"
                disabled={verifyLoading || resendLoading}
                value={otp}
                onChange={(e) => setOTP(e.target.value)}
                placeholder="Enter 6-digit code"
              />
            </div>
            <div className={style.buttonsContainer}>
              <button
                type="submit"
                disabled={verifyLoading || resendLoading || isExpired}
                onClick={handleSubmit}
              >
                {verifyLoading ? (
                  <ClipLoader size={13} color="#fff" />
                ) : (
                  "Verify"
                )}
              </button>
              <button
                type="submit"
                disabled={verifyLoading || resendLoading}
                onClick={handleResend}
              >
                {resendLoading ? (
                  <ClipLoader size={13} color="#fff" />
                ) : (
                  "Resend"
                )}
              </button>
            </div>
          </div>
        </div>
        <div
          className={`${style.timerContainer} ${isExpired && style.expired}`}
        >
          {expiryTimestamp && (
            <OTPTimer
              expiryTimestamp={expiryTimestamp}
              onExpire={() => setIsExpired(true)}
            />
          )}
        </div>
      </div>
      {/* Notification Component */}
      <Notification isVisible={visible} response={response} />
    </div>
  );
}

export default ResendAndVerifyOTP;
