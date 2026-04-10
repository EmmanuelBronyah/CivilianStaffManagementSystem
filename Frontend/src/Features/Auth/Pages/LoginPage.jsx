import { useEffect, useState } from "react";
import api from "../../../api";
import { useNavigate, Link } from "react-router-dom";
import checkTaskStatus from "../../../utils/checkOtpStatus";
import checkInternetConnection from "../../../utils/checkInternetConnection";
import getResponseMessages from "../../../utils/extractResponseMessage";
import style from "../../../styles/pages/loginscreen.module.css";
import image from "../../../assets/images/image.svg";
import darkImage from "../../../assets/images/darkImage.svg";
import ClipLoader from "react-spinners/ClipLoader";
import Notification from "../../../Components/Common/NotificationComponent";
import ThemeToggle from "../../../Components/Common/ThemeToggleComponent";
import { useTheme } from "../../../context/ThemeContext";
import { MdVisibility, MdVisibilityOff } from "react-icons/md";

function LoginUser(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [selectedRole, setSelectedRole] = useState("Standard User");
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { theme } = useTheme();

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
        message:
          "Network issue detected - Please ensure you are connected to the internet and try again",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    if (!username || !password) {
      setIsLoading(false);
      setResponse({
        message: "Username and password are required",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    try {
      const res = await api.post(props.route, {
        username,
        password,
        selectedRole,
      });

      if (res.status === 200) {
        const message = getResponseMessages(res);
        if (message && message === "OTP already sent") {
          setResponse({
            message: "OTP already sent",
          });
          return;
        }

        const otpTaskId = res.data.task_id;
        localStorage.setItem("otpTaskId", otpTaskId);

        const tempToken = res.data.temp_token;

        checkTaskStatus(setResponse, setIsLoading, tempToken, navigate);
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
    <div className={`${style.loginPage} ${!theme && style.dark}`}>
      {/* LOGO SECTION */}
      <div className={style.logoAndSwitchContainer}>
        <div className={style.emptyDiv}></div>
        <p>CiviBase</p>
        <ThemeToggle className={style.switch} />
      </div>
      {/* IMAGE AND LOGIN FORM GRID */}
      <div className={style.imageFormGrid}>
        {/* IMAGE SECTION */}
        <div className={style.imageContainer}>
          <img
            src={`${!theme ? darkImage : image}`}
            loading="lazy"
            alt="Login Illustration"
          />
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
                  type={`${showPassword ? "text" : "password"}`}
                  value={password}
                  disabled={isLoading}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                />
                <MdVisibility
                  className={`${style.passwordVisible} ${showPassword ? "" : style.hidden}`}
                  onClick={() => setShowPassword((prevState) => !prevState)}
                />
                <MdVisibilityOff
                  className={`${style.passwordInvisible} ${showPassword ? style.hidden : ""}`}
                  onClick={() => setShowPassword((prevState) => !prevState)}
                />
              </div>

              <div className={style.roleContainer}>
                <h4>Role</h4>
                <div className={style.roleDiv}>{selectedRole}</div>
              </div>

              <div className={style.buttonContainer}>
                <button
                  type="submit"
                  disabled={isLoading}
                  className={`${style.loginButton} ${isLoading ? style.disabled : ""}`}
                >
                  {isLoading ? (
                    <ClipLoader
                      size={25}
                      color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                    />
                  ) : (
                    "Login"
                  )}
                </button>
              </div>
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
