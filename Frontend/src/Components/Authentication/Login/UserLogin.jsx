import { useEffect, useState } from "react";
import api from "../../../api";
import { TEMP_TOKEN } from "../../../constants";
import { useNavigate, Link } from "react-router-dom";
import { checkInternetConnection } from "../../../utils";
import style from "../../../styles/loginscreen.module.css";
import image from "../../../images/image.svg";

function LoginUser({ route }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.clear();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      console.log(
        "Network issue detected. Please ensure you are connected to the internet and try again.",
      );
      return;
    }

    try {
      const res = await api.post(route, {
        username,
        password,
      });
      if (res.status === 200) {
        if (localStorage.getItem(TEMP_TOKEN)) {
          console.log("Response: ", res.data.detail);
        } else {
          localStorage.setItem(TEMP_TOKEN, res.data.temp_token);
          console.log("Response: ", res.data.detail);
        }

        navigate("/auth/otp");
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
    <div className={style.loginPage}>
      {/* LOGO SECTION */}
      <div className={style.logoText}>CiviBase</div>
      {/* IMAGE AND LOGIN FORM GRID */}
      <div className={style.imageFormGrid}>
        {/* IMAGE SECTION */}
        <div className={style.imageContainer}>
          <img src={image} alt="" />
        </div>
        {/* LOGIN FORM SECTION */}
        <div className={style.loginForm}>
          <form onSubmit={handleSubmit}>
            <div className={style.textButtonContainer}>
              <h3>Login as</h3>
              <div className={style.buttonContainer}>
                <button>Admin User</button>
                <button>Standard User</button>
                <button>Viewer</button>
              </div>
            </div>
            <div className={style.usernameTextbox}>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />
            </div>
            <div className={style.passwordTextbox}>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
              />
            </div>

            <div className={style.roleContainer}>
              <h4>Role</h4>
              <div className={style.roleDiv}>Standard User</div>
            </div>

            <button type="submit" className={style.loginButton}>
              Login
            </button>
          </form>
          <div className={style.forgotPassword}>
            <Link to="/reset-password">Forgot Password?</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginUser;
