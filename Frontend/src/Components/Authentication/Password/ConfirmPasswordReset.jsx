import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../../api";
import { checkInternetConnection } from "../../../utils";

function ConfirmPasswordReset({ route }) {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();
  const { uid, token } = useParams();

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
        uid: uid,
        token: token,
        new_password1: password,
        new_password2: confirmPassword,
      });
      if (res.status === 200) {
        console.log("Response: ", res.data.detail);
        navigate("/auth/login");
      }
    } catch (error) {
      if (error.response) {
        console.log("Error: ", error.response.data);
      } else {
        console.log("Unexpected Error: ", error);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="New Password"
        />
      </div>
      <div>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

export default ConfirmPasswordReset;
