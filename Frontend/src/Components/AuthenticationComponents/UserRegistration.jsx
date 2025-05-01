import { useState } from "react";
import api from "../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constants";
import { useNavigate } from "react-router-dom";

function RegisterUser({ route }) {
  const [fullname, setFullname] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [grade, setGrade] = useState("");
  const [division, setDivision] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post(route, {
        fullname,
        username,
        email,
        password,
        role,
        grade,
        division,
      });
      if (res.status === 201) {
        navigate("/auth/login");
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
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
