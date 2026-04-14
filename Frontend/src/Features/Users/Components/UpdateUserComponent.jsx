import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import { useState, useEffect } from "react";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import Notification from "../../../Components/Common/NotificationComponent";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";

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
  });
  const [formData, setFormData] = useState({});
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
        setInitialData({
          fullName: res.data.fullname,
          username: res.data.username,
          email: res.data.email,
          oldPassword: "",
          newPassword: "",
          role: dropdownRoleValue(res.data.role),
          grade: { value: res.data.grade_id, label: res.data.grade_display },
          division: {
            value: res.data.division_id,
            label: res.data.division_display,
          },
        });
      } catch (error) {
        console.log(error.response);

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

  const updateUser = () => {
    return;
  };

  const clearData = () => {
    // setFormData(initialFormData);
    return;
  };

  return (
    <>
      <div
        className={`${style.updateUserComponentContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.allUsersButtonContainer}>
          <button onClick={() => setUserPage("All Users")}>All Users</button>
        </div>
        <div className={style.updateUserContainer}>
          <div className={style.titleButtonContainer}>
            <p>Update User Info</p>
            <button>Reactivate Account</button>
          </div>
          <AddUserInputBoxes
            userPage={userPage}
            formData={formData}
            setFormData={setFormData}
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
              <button disabled={loading} onClick={clearData}>
                Cancel
              </button>
            </div>
          </div>
        </div>
        <div className={style.danger}>
          <p>Danger Zone</p>
          <div className={style.deactivate}>
            <p>
              Temporarily disable this user's access. You can reactivate them at
              any time.
            </p>
            <button className={style.deactivate}>Deactivate Account</button>
          </div>
          <div className={style.delete}>
            <p>
              This action is irreversible. All user data will be permanently
              removed.
            </p>
            <button className={style.delete}>Delete User</button>
          </div>
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
