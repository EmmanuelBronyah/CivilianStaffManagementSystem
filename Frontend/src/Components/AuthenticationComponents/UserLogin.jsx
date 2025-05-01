import { useState } from "react";
import api from "../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../../constants";
import { useNavigate } from "react-router-dom";

function LoginUser({ route }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post(route, {
        username,
        password,
      });
      if (res.status === 200) {
        localStorage.setItem(TEMP_TOKEN, res.data.temp_token);
        navigate("/auth/otp");
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
  );
}

export default LoginUser;
