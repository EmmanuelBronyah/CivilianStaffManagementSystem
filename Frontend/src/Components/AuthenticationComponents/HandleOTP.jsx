import { useState } from "react";
import api from "../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../../constants";
import { useNavigate } from "react-router-dom";

function ResendAndVerifyOTP({ route }) {
  const [otp, setOTP] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tokenData = { tokens: { temp_token: temp_token, otp_token: otp } };

    try {
      const res = await api.post(route, tokenData);
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
        localStorage.removeItem(TEMP_TOKEN);
        navigate("/dashboard");
      }
    } catch (error) {
      alert(
        `ERROR STATUS: ${error.response.status}|ERROR DATA: ${JSON.stringify(
          error.response.data
        )}`
      );
    }
  };

  const handleResend = async (e) => {
    e.preventDefault();
    const otpResendRoute = "api/resend-otp/";
    const temp_token = localStorage.getItem(TEMP_TOKEN);
    const tempTokenData = { tokens: { temp_token: temp_token } };

    try {
      const res = await api.post(otpResendRoute, tempTokenData);
      if (res.status === 200) {
        localStorage.setItem(TEMP_TOKEN);
        handleSubmit();
      }
    } catch (error) {
      alert(
        `ERROR STATUS: ${error.response.status}|ERROR DATA: ${JSON.stringify(
          error.response.data
        )}`
      );
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
