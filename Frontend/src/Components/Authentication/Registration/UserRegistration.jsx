import { useState } from "react";
import api from "../../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../../constants";
import { useNavigate } from "react-router-dom";
import { checkInternetConnection } from "../../../utils";

function RegisterUser({ route }) {
  const [fullname, setFullname] = useState("");
  const [username, setUsername] = useState("");
  const [user_email, setUserEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [grade, setGrade] = useState("");
  const [division, setDivision] = useState("");
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
        fullname,
        username,
        user_email,
        password,
        role,
        grade,
        division,
      });
      if (res.status === 201) {
        console.log("Response: ", "User created successfully.");

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
    // TODO :=> CONFIRM PASSWORD TEXT INPUT

    <form onSubmit={handleSubmit}>
      <h1>Registration Form</h1>
      <div>
        <input
          type="text"
          value={fullname}
          onChange={(e) => setFullname(e.target.value)}
          placeholder="Fullname"
        />
      </div>

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
          type="email"
          value={user_email}
          onChange={(e) => setUserEmail(e.target.value)}
          placeholder="Email address"
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

      <div>
        <input
          type="text"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          placeholder="Role"
        />
      </div>

      <div>
        <input
          type="text"
          value={grade}
          onChange={(e) => setGrade(e.target.value)}
          placeholder="Grade"
        />
      </div>

      <div>
        <input
          type="text"
          value={division}
          onChange={(e) => setDivision(e.target.value)}
          placeholder="Division"
        />
      </div>

      <button type="submit">Register</button>
    </form>
  );
}

export default RegisterUser;
