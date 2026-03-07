import api from "../api";
import getResponseMessages from "./extractResponseMessage";
import { TEMP_TOKEN } from "../constants";

export default function checkTaskStatus(
  setResponse,
  setIsLoading,
  tempToken,
  navigate,
) {
  const otpTaskId = localStorage.getItem("otpTaskId");

  const interval = setInterval(async () => {
    try {
      const res = await api.get(`/api/task-status/${otpTaskId}/`);

      if (res.data.status === "SUCCESS") {
        clearInterval(interval);

        if (!localStorage.getItem(TEMP_TOKEN)) {
          localStorage.setItem(TEMP_TOKEN, tempToken);
        }

        setIsLoading(false);
        setResponse({
          message: "OTP sent to your email",
        });

        setTimeout(() => {
          navigate("/auth/otp");
        }, 4000);
      }
      if (res.data.status === "FAILURE") {
        clearInterval(interval);

        setResponse({
          message: "Failed to send OTP",
          type: "error",
        });

        setIsLoading(false);
      }
    } catch (error) {
      clearInterval(interval);

      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });

      setIsLoading(false);
    }
  }, 2000);
}
