import { useState } from "react";
import api from "../../../api";
import { TEMP_TOKEN } from "../../../constants";
import { useNavigate, Link } from "react-router-dom";
import { extractErrorMessages, checkInternetConnection } from "../../../utils";

function LoginUser({ route }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      console.log(
        "Network issue detected. Please ensure you are connected to the internet and try again."
      );
      return;
    }

    try {
      const res = await api.post(route, {
        username,
        password,
      });
      if (res.status === 200) {
        localStorage.setItem(TEMP_TOKEN, res.data.temp_token);
        console.log(res.data);

        navigate("/auth/otp");
      }
    } catch (error) {
      let errorData = error.response.data;
      const messages = extractErrorMessages(errorData);
      for (const message of messages) {
        console.log("Error message:", message);
      }
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <h1>Login Form</h1>
        <div>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
        </div>

        <div>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
        </div>

        <button type="submit">Login</button>
      </form>
      <Link to="/reset-password">Forgot Password?</Link>
    </>
  );
}

export default LoginUser;
