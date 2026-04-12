import api from "../../../api";
import { useEffect, useState } from "react";
import { useTheme } from "../../../Context/ThemeContext";
import style from "../../../styles/components/userscomponent.module.css";
import Notification from "../../../Components/Common/NotificationComponent";
import getResponseMessages from "../../../utils/extractResponseMessage";
import UsersPerDivision from "./UsersPerDivisionComponent";

export default function AllUsersComponent({ setUserPage }) {
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [usersPerDivision, setUsersPerDivision] = useState([]);

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
    const fetchUsersPerDivision = async () => {
      try {
        const res = await api.get("api/divisions/users/");
        setUsersPerDivision(res.data);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };

    fetchUsersPerDivision();
  }, []);

  return (
    <>
      <div className={`${style.allUsersContainer} ${!theme ? style.dark : ""}`}>
        <div className={style.titleButtonSection}>
          <div className={style.title}>
            <p>User Management</p>
          </div>
          <button onClick={() => setUserPage("Add User")}>Add User</button>
        </div>
        <div className={style.divisions}>
          <UsersPerDivision usersPerDivision={usersPerDivision} />
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
