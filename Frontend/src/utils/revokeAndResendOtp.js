import api from "../api";
import { TEMP_TOKEN } from "../constants";
import getResponseMessages from "./extractResponseMessage";
import checkResendOtpTaskStatus from "./checkResendOtpStatus";

export default async function handleRevokeAndResendOTP(
  setResponse,
  setResendIsLoading,
  setResetTimer,
) {
  const otpTaskId = localStorage.getItem("otpTaskId");

  const otpResendRoute = "api/resend-otp/";
  const temp_token = localStorage.getItem(TEMP_TOKEN);
  const tempTokenData = { tokens: { temp_token: temp_token } };

  try {
    const deleteTaskResponse = await api.delete(
      `/api/task-delete/${otpTaskId}/`,
    );
    if (deleteTaskResponse.status === 200) {
      const resendOtpResponse = await api.post(otpResendRoute, tempTokenData);

      if (resendOtpResponse.status === 200) {
        const message = getResponseMessages(resendOtpResponse);

        if (message && message === "OTP already sent") {
          setResendIsLoading(false);

          setResponse({
            message: "OTP already sent",
            id: Date.now(),
          });
          return;
        }

        const tempToken = resendOtpResponse.data.temp_token;
        localStorage.setItem(TEMP_TOKEN, tempToken);

        const taskId = resendOtpResponse.data.task_id;
        localStorage.setItem("otpTaskId", taskId);

        checkResendOtpTaskStatus(
          setResponse,
          setResendIsLoading,
          setResetTimer,
          taskId,
        );
      }
    }
  } catch (error) {
    setResendIsLoading(false);

    setResponse({
      message: getResponseMessages(error.response),
      type: "error",
      id: Date.now(),
    });
  }
}
