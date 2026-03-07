import api from "../api";
import getResponseMessages from "./extractResponseMessage";

export default function checkResendOtpTaskStatus(
  setResponse,
  setResendIsLoading,
  setResetTimer,
  taskId,
) {
  const interval = setInterval(async () => {
    try {
      const res = await api.get(`/api/task-status/${taskId}/`);

      if (res.data.status === "SUCCESS") {
        clearInterval(interval);

        setResendIsLoading(false);

        // Re-start timer at the moment OTP is sent
        setResetTimer(true);

        setResponse({
          message: "OTP sent to your email",
        });
      }
      if (res.data.status === "FAILURE") {
        clearInterval(interval);

        setResendIsLoading(false);

        setResponse({
          message: "Failed to send OTP",
          type: "error",
        });
      }
    } catch (error) {
      clearInterval(interval);

      setResendIsLoading(false);

      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
    }
  }, 2000);
}
