import api from "../api";
import getResponseMessages from "./extractResponseMessage";

export default function checkResendOtpTaskStatus(
  setResponse,
  setResendIsLoading,
  taskId,
) {
  const interval = setInterval(async () => {
    try {
      const res = await api.get(`/api/task-status/${taskId}/`);

      if (res.data.status === "SUCCESS") {
        console.log("OTP RESEND WAS A SUCCESS");

        clearInterval(interval);

        setResendIsLoading(false);
        setResponse({
          message: "OTP sent to your email.",
        });
      }
      if (res.data.status === "FAILURE") {
        console.log("OTP RESEND WAS A FAILURE");

        clearInterval(interval);

        setResponse({
          message: "Failed to send OTP.",
          type: "error",
        });

        setResendIsLoading(false);
      }
    } catch (error) {
      console.log("THERE WAS AN ERROR IN OTP RESEND");
      clearInterval(interval);

      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });

      setResendIsLoading(false);
    }
  }, 2000);
}
