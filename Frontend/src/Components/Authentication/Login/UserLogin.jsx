import { useEffect, useState } from "react";
import api from "../../../api";
import { TEMP_TOKEN } from "../../../constants";
import { useNavigate, Link } from "react-router-dom";
import { checkInternetConnection, getResponseMessages } from "../../../utils";
import style from "../../../styles/loginscreen.module.css";
import image from "../../../images/image.svg";
import ClipLoader from "react-spinners/ClipLoader";

function LoginUser({ route }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [selectedRole, setSelectedRole] = useState("Standard User");
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const navigate = useNavigate();

  const roles = ["Administrator", "Standard User", "Viewer"];

  useEffect(() => {
    localStorage.clear();
  }, []);

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    const hasInternetConnection = await checkInternetConnection();

    if (!hasInternetConnection) {
      setIsLoading(false);
      setResponse({
        message: "Network issue detected. Please ensure you are connected.",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      const res = await api.post(route, {
        username,
        password,
        selectedRole,
      });

      const tempToken = res.data.temp_token;

      if (!localStorage.getItem(TEMP_TOKEN)) {
        localStorage.setItem(TEMP_TOKEN, tempToken);
      }

      setResponse({
        message: getResponseMessages(res),
        type: "success",
        id: Date.now(),
      });

      setTimeout(() => {
        navigate("/auth/otp");
      }, 3000);
    } catch (error) {
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
    } finally {
      setIsLoading(false);
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
          <img src={image} loading="lazy" alt="" />
        </div>
        {/* LOGIN FORM SECTION */}
        <div className={style.loginForm}>
          <form onSubmit={handleSubmit}>
            <div className={style.textRolesContainer}>
              <h3>Login as</h3>
              <div className={style.rolesContainer}>
                {roles.map((role) => (
                  <div
                    key={role}
                    onClick={() => setSelectedRole(role)}
                    className={selectedRole === role ? style.activeRole : ""}
                  >
                    {role}
                  </div>
                ))}
              </div>
            </div>
            <div className={style.usernameTextbox}>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                className={`${isLoading ? style.disabled : ""}`}
              />
            </div>
            <div className={style.passwordTextbox}>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className={`${isLoading ? style.disabled : ""}`}
              />
            </div>

            <div className={style.roleContainer}>
              <h4>Role</h4>
              <div className={style.roleDiv}>{selectedRole}</div>
            </div>

            <button
              type="submit"
              className={`${style.loginButton} ${isLoading ? style.disabled : ""}`}
            >
              {isLoading ? <ClipLoader size={18} color="#fff" /> : "Login"}
            </button>
          </form>
          <div
            className={`${selectedRole === "Administrator" ? style.forgotPassword : style.forgotPasswordDisabled}`}
          >
            <Link to="/reset-password">Forgot Password?</Link>
          </div>
        </div>
      </div>
      <div
        className={`${style.notificationContainer} ${
          visible ? style.show : ""
        } ${response?.type === "error" ? style.error : ""}`}
      >
        {response?.message}
      </div>
    </div>
  );
}

export default LoginUser;
