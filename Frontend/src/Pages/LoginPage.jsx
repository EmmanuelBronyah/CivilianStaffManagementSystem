import { useEffect, useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";
import checkTaskStatus from "../utils/checkOtpStatus";
import checkInternetConnection from "../utils/checkInternetConnection";
import getResponseMessages from "../utils/extractResponseMessage";
import style from "../styles/pages/loginscreen.module.css";
import image from "../images/image.svg";
import ClipLoader from "react-spinners/ClipLoader";
import Notification from "../Components/NotificationComponent";

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

    if (!username || !password) {
      setIsLoading(false);
      setResponse({
        message: "Username and password are required.",
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

      if (res.status === 200) {
        const message = getResponseMessages(res);
        if (message && message === "OTP already sent.") {
          setResponse({
            message: "OTP already sent.",
          });
          return;
        }

        const otpTaskId = res.data.task_id;
        const tempToken = res.data.temp_token;

        checkTaskStatus(
          otpTaskId,
          setResponse,
          setIsLoading,
          tempToken,
          navigate,
        );
      }
    } catch (error) {
      setIsLoading(false);
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });
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
          <img src={image} loading="lazy" alt="Login Illustration" />
        </div>
        {/* LOGIN FORM SECTION */}
        <div className={style.loginForm}>
          <div className={style.formWrapper}>
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
                      <h3>{role}</h3>
                    </div>
                  ))}
                </div>
              </div>
              <div className={style.usernameTextbox}>
                <input
                  type="text"
                  value={username}
                  disabled={isLoading}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Username"
                />
              </div>
              <div className={style.passwordTextbox}>
                <input
                  type="password"
                  value={password}
                  disabled={isLoading}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                />
              </div>

              <div className={style.roleContainer}>
                <h4>Role</h4>
                <div className={style.roleDiv}>{selectedRole}</div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
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
      </div>

      {/* Notification Component */}
      <Notification isVisible={visible} response={response} />
    </div>
  );
}

export default LoginUser;
