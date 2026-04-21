import style from "../../../styles/components/userscomponent.module.css";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import { useTheme } from "../../../Context/ThemeContext";
import { useState, useEffect } from "react";
import Notification from "../../../Components/Common/NotificationComponent";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";
import verifyAdminProcess, {
  showErrorModal,
} from "../../../utils/askAdminIdentity";

export default function AddUsersComponent({ setUserPage }) {
  const initialFormData = {
    fullName: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: null,
    grade: null,
    division: null,
  };
  const [formData, setFormData] = useState(initialFormData);
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;

    setVisible(true);

    const timer = setTimeout(() => {
      setVisible(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, [response]);

  const registerUser = async () => {
    const data = Object.values(formData);

    if (
      data.some(
        (value) =>
          value === null ||
          value === "" ||
          (typeof value === "string" && value.trim() === ""),
      )
    ) {
      setResponse({
        message: "All fields are required",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setResponse({
        message: "Passwords do not match",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    const status = await verifyAdminProcess(theme, setLoading, setResponse);

    if (status === 401) {
      await showErrorModal(theme);
      return;
    } else if (status === 200) {
      const payload = {
        fullname: formData.fullName,
        password: formData.password,
        username: formData.username,
        email: formData.email,
        role: formData.role?.label || "",
        grade: formData.grade?.value || null,
        division: formData.division?.value || null,
      };

      try {
        const res = await api.post("api/register/", payload);
        if (res.status === 201) {
          setLoading(false);
          setResponse({
            message: "User Account created",
            id: Date.now(),
          });
          setFormData(initialFormData);
          return;
        }
      } catch (error) {
        setLoading(false);
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    }
  };

  const clearData = () => {
    setFormData(initialFormData);
    return;
  };

  return (
    <>
      <div
        className={`${style.addUserComponentContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.allUsersButtonContainer}>
          <button onClick={() => setUserPage("All Users")}>All Users</button>
        </div>
        <div className={style.addUserContainer}>
          <div className={style.addUserTitle}>
            <p>Add A New User</p>
          </div>
          <AddUserInputBoxes
            formData={formData}
            setFormData={setFormData}
            setResponse={setResponse}
          />
          <div className={style.buttonsContainer}>
            <div className={style.addUserButton}>
              <button disabled={loading} onClick={registerUser}>
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save"
                )}
              </button>
            </div>

            <div className={style.discardButton}>
              <button disabled={loading} onClick={clearData}>
                Discard
              </button>
            </div>
          </div>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
