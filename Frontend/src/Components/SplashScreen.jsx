import { useNavigate } from "react-router-dom";

function SplashScreen() {
  const navigate = useNavigate();

  function handleRegisterRedirect() {
    navigate("/auth/register");
  }

  function handleLoginRedirect() {
    navigate("/auth/login");
  }

  return (
    <>
      <h1>CiviBase</h1>
      <button onClick={handleRegisterRedirect}>Register</button>
      <button onClick={handleLoginRedirect}>Login</button>
    </>
  );
}

export default SplashScreen;
