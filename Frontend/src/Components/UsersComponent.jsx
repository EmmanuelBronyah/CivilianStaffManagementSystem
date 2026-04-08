import style from "../styles/components/userscomponent.module.css";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import { useTheme } from "../context/ThemeContext";
import { useState, useEffect } from "react";
import Notification from "../Components/NotificationComponent";

export default function Users() {
  const [formData, setFormData] = useState({
    fullName: "",
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: null,
    grade: null,
    division: null,
  });
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);

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

    const payload = {
      fullname: formData.fullName,
      password: formData.password,
      username: formData.username,
      email: formData.email,
      role: formData.role?.label || "",
      grade: formData.grade?.value || null,
      division: formData.division?.value || null,
    };
    console.log("formData", payload);
  };

  return (
    <main
      className={`${style.addUserComponentContainer} ${!theme ? style.dark : ""}`}
    >
      <div className={style.allUsersButtonContainer}>
        <button>All Users</button>
      </div>
      <div className={style.addUserContainer}>
        <div className={style.addUserTitle}>
          <p>Add A New User</p>
        </div>
        <AddUserInputBoxes formData={formData} setFormData={setFormData} />
        <div className={style.buttonsContainer}>
          <div className={style.addUserButton}>
            <button onClick={registerUser}>Save</button>
          </div>
          <div className={style.addUserButton}>
            <button>Save & Add Another</button>
          </div>
          <div className={style.discardButton}>
            <button>Discard</button>
          </div>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </main>
  );
}
