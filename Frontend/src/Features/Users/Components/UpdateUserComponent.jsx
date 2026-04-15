import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import { useState, useEffect } from "react";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import Notification from "../../../Components/Common/NotificationComponent";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import verifyAdminProcess, {
  showErrorModal,
} from "../../../utils/askAdminIdentity";
import ClipLoader from "react-spinners/ClipLoader";
import manageUserAccessProcess from "../../../utils/manageUserAccess";
import ReadOnlyUserData from "./AddReadOnlyUserData";

export default function UpdateUser({ userPage, setUserPage, userId }) {
  const [initialData, setInitialData] = useState({
    fullName: "",
    username: "",
    email: "",
    oldPassword: "",
    newPassword: "",
    role: "",
    grade: "",
    division: "",
    createdAt: "",
    updatedAt: "",
    createdBy: "",
    updatedBy: "",
  });
  const [formData, setFormData] = useState({});
  const [active, setActive] = useState(true);
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

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  const dropdownRoleValue = (role) => {
    switch (role) {
      case "ADMINISTRATOR":
        return { value: 1, label: "ADMINISTRATOR" };
      case "STANDARD USER":
        return { value: 2, label: "STANDARD USER" };
      case "VIEWER":
        return { value: 3, label: "VIEWER" };
      default:
        break;
    }
  };

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get(`api/users/${userId}/`);
        console.log(res.data);

        setActive(res.data.is_active);

        setInitialData({
          fullName: res.data.fullname,
          username: res.data.username,
          email: res.data.email,
          oldPassword: "",
          newPassword: "",
          role: dropdownRoleValue(res.data.role),
          grade: { value: res.data.grade, label: res.data.grade_display },
          division: {
            value: res.data.division,
            label: res.data.division_display,
          },
          createdAt: res.data.created_at,
          updatedAt: res.data.updated_at,
          createdBy: res.data.created_by_display,
          updatedBy: res.data.updated_by_display,
        });
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };

    fetchUser();
  }, []);

  const updateUser = async () => {
    const {
      fullName,
      username,
      email,
      role: { label: roleName },
      grade: { value: gradeId },
      division: { value: divisionId },
    } = formData;

    const data = [fullName, username, email, roleName, gradeId, divisionId];

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

    const status = await verifyAdminProcess(theme, setLoading, setResponse);

    if (status === 401) {
      await showErrorModal(theme);
      return;
    } else if (status === 200) {
      const payload = {
        fullname: fullName,
        username: username,
        email: email,
        role: roleName,
        grade: gradeId,
        division: divisionId,
      };

      try {
        const res = await api.patch(`api/users/update/${userId}/`, payload);
        if (res.status === 200) {
          setLoading(false);
          setResponse({
            message: "User Account updated",
            id: Date.now(),
          });
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

  const resetData = () => {
    setFormData(initialData);
    return;
  };

  const initiateDeactivateUserProcess = async () => {
    const result = await manageUserAccessProcess(
      theme,
      "deactivate",
      userId,
      setLoading,
      setResponse,
      "User Account Deactivation",
      "Are you sure you want to temporarily disable this user's access?",
    );
    if (result === "DEACTIVATED | RESTORED") {
      setActive(false);
    }
  };

  const initiateRestoreUserProcess = async () => {
    const result = await manageUserAccessProcess(
      theme,
      "restore",
      userId,
      setLoading,
      setResponse,
      "Restore User Account",
      "Are you sure you want to re-enable this user's access?",
    );
    if (result === "DEACTIVATED | RESTORED") {
      setActive(true);
    }
  };

  const initiateDeleteUserProcess = async () => {
    const result = await manageUserAccessProcess(
      theme,
      "delete",
      userId,
      setLoading,
      setResponse,
      "User Account Deletion",
      "Are you sure you want to permanently delete this user's account?",
    );
    if (result === "DELETED") {
      setUserPage("All Users");
    }
  };

  const initiatePasswordReset = async () => {
    await manageUserAccessProcess(
      theme,
      "passwordReset",
      userId,
      setLoading,
      setResponse,
      "User Account Password Reset",
      "Are you sure you want to send a password reset link to this user's email?",
      initialData.email,
    );
  };

  return (
    <>
      <div
        className={`${style.updateUserComponentContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.allUsersButtonContainer}>
          <button disabled={loading} onClick={() => setUserPage("All Users")}>
            All Users
          </button>
        </div>
        <div className={style.updateUserContainer}>
          <div className={style.titleButtonContainer}>
            <p>Update User Info</p>
            {!active && (
              <button
                className={style.restoreButton}
                disabled={loading}
                onClick={initiateRestoreUserProcess}
              >
                Restore Account
              </button>
            )}
          </div>
          <AddUserInputBoxes
            userPage={userPage}
            formData={formData}
            setFormData={setFormData}
            initialData={initialData}
          />
          <div className={style.buttonsContainer}>
            <div className={style.addUserButton}>
              <button disabled={loading} onClick={updateUser}>
                {loading ? (
                  <ClipLoader
                    size={13}
                    color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                  />
                ) : (
                  "Save Changes"
                )}
              </button>
            </div>
            <div className={style.discardButton}>
              <button disabled={loading} onClick={resetData}>
                Cancel
              </button>
            </div>
            <p onClick={initiatePasswordReset}>Reset Password?</p>
          </div>
        </div>
        <div className={style.danger}>
          <p>Danger Zone</p>
          <div
            className={`${style.deactivate} ${active ? "" : style.displayNone}`}
          >
            <p>
              Temporarily disable this user's access. You can reactivate them at
              any time.
            </p>
            <button
              onClick={initiateDeactivateUserProcess}
              disabled={loading}
              className={style.deactivate}
            >
              Deactivate Account
            </button>
          </div>
          <div className={style.delete}>
            <p>
              This action is irreversible. All user data will be permanently
              removed.
            </p>
            <button
              onClick={initiateDeleteUserProcess}
              disabled={loading}
              className={style.delete}
            >
              Delete User
            </button>
          </div>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
