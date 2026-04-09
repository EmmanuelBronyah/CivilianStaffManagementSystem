import style from "../styles/components/userscomponent.module.css";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import { useTheme } from "../context/ThemeContext";
import { useState, useEffect } from "react";
import Notification from "../Components/NotificationComponent";
import Swal from "sweetalert2";
import { USER_ID } from "../constants";
import api from "../api";
import getResponseMessages from "../utils/extractResponseMessage";
import ClipLoader from "react-spinners/ClipLoader";

export default function Users() {
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

  const askForAdminPassword = async () => {
    const result = await Swal.fire({
      title: "Confirm Admin Password",
      input: "password",
      inputLabel: "Enter your password to continue",
      inputPlaceholder: "Enter password",
      inputAttributes: {
        autocapitalize: "off",
        autocorrect: "off",
      },
      showCancelButton: true,
      confirmButtonText: "Verify",

      customClass: {
        popup: `${style.customModal} ${!theme ? style.dark : ""}`,
        title: `${style.customTitle} ${!theme ? style.dark : ""}`,
        confirmButton: `${style.customConfirmBtn} ${!theme ? style.dark : ""}`,
        cancelButton: `${style.customCancelBtn} ${!theme ? style.dark : ""}`,
        input: `${style.customInput} ${!theme ? style.dark : ""}`,
      },
    });

    return result;
  };

  const showErrorModal = async () => {
    await Swal.fire({
      title: "Error",
      text: "Invalid Credentials",
      icon: "error",
      confirmButtonText: "OK",

      customClass: {
        popup: `${style.customModal} ${!theme ? style.dark : ""}`,
        title: `${style.customTitle} ${!theme ? style.dark : ""}`,
        confirmButton: `${style.customConfirmBtn} ${!theme ? style.dark : ""}`,
      },
    });
  };

  const verifyAdminIdentity = async (verificationData) => {
    try {
      await api.post("api/users/verify/admin/", { data: verificationData });
    } catch (error) {
      if (error.response.status === 401) {
        return error.response.status;
      } else {
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

  const registerUser = async () => {
    setLoading(true);

    const data = Object.values(formData);

    if (
      data.some(
        (value) =>
          value === null ||
          value === "" ||
          (typeof value === "string" && value.trim() === ""),
      )
    ) {
      setLoading(false);
      setResponse({
        message: "All fields are required",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setLoading(false);
      setResponse({
        message: "Passwords do not match",
        type: "error",
        id: Date.now(),
      });
      return;
    }

    const result = await askForAdminPassword();

    if (!result.isConfirmed) return;

    const userID = localStorage.getItem(USER_ID);
    const verificationData = {
      id: userID,
      adminPassword: result.value,
    };

    const status = await verifyAdminIdentity(verificationData);

    if (status === 401) {
      setLoading(false);
      await showErrorModal();
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
  };

  const clearData = () => {
    setFormData(initialFormData);
    return;
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
            <button onClick={registerUser}>
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
            <button onClick={clearData}>Discard</button>
          </div>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </main>
  );
}
