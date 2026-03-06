import Countdown from "react-countdown";

function OTPTimer({ expiryTimestamp, onExpire }) {
  return (
    <Countdown
      date={expiryTimestamp}
      renderer={({ minutes, seconds, completed }) => {
        if (completed) {
          onExpire && onExpire();
          localStorage.clear();
          return (
            <span>OTP has expired. Please start the login process again.</span>
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
