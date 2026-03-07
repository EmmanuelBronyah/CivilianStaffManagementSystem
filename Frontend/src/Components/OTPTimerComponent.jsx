import Countdown from "react-countdown";
import { useNavigate } from "react-router-dom";

function OTPTimer({ expiryTimestamp, onExpire }) {
  const navigate = useNavigate();
  return (
    <Countdown
      date={expiryTimestamp}
      renderer={({ minutes, seconds, completed }) => {
        if (completed) {
          onExpire && onExpire();

          localStorage.clear();

          setTimeout(() => {
            navigate("/auth/login");
          }, 3000);

          return (
            <span>OTP has expired - Please start the login process again</span>
          );
        }

        return (
          <span>
            Expires in: {minutes}:{seconds < 10 ? "0" : ""}
            {seconds}
          </span>
        );
      }}
    />
  );
}

export default OTPTimer;
