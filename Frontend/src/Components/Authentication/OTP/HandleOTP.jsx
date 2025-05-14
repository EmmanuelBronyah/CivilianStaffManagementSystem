import { useState } from "react";
import api from "../../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../../../constants";
import { useNavigate } from "react-router-dom";
import { extractErrorMessages, checkInternetConnection } from "../../../utils";

function ResendAndVerifyOTP({ route }) {
  const [otp, setOTP] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tokenData = { tokens: { temp_token: temp_token, otp_token: otp } };
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      console.log(
        "Network issue detected. Please ensure you are connected to the internet and try again."
      );
      return;
    }

    try {
      const res = await api.post(route, tokenData);
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        localStorage.removeItem(TEMP_TOKEN);
        navigate("/dashboard");
      }
    } catch (error) {
      // let errorData = error.response;
      console.log("Error message:", error.response.data);
      // const messages = extractErrorMessages(errorData);
      // for (const message of messages) {
      //   console.log("Error message:", message);
      // }
    }
  };

  const handleResend = async (e) => {
    e.preventDefault();
    const otpResendRoute = "api/resend-otp/";
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tempTokenData = { tokens: { temp_token: temp_token } };
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      console.log(
        "Network issue detected. Please ensure you are connected to the internet and try again."
      );
      return;
    }

    try {
      const res = await api.post(otpResendRoute, tempTokenData);
      if (res.status === 200) {
        const tempToken = res.data.temp_token;
        localStorage.setItem(TEMP_TOKEN, tempToken);
        console.log(res.data);
      }
    } catch (error) {
      // let errorData = error.response;
      console.log("Error message:", error.response.data);
      // const messages = extractErrorMessages(errorData);
      // for (const message of messages) {
      //   console.log("Error message:", message);
      // }
    }
  };

  return (
    <>
      <h1>OTP Form</h1>
      <input
        type="text"
        value={otp}
        onChange={(e) => setOTP(e.target.value)}
        placeholder="OTP"
      />

      <button type="submit" onClick={handleSubmit}>
        Verify
      </button>
      <button type="submit" onClick={handleResend}>
        Resend
      </button>
    </>
  );
}

export default ResendAndVerifyOTP;
