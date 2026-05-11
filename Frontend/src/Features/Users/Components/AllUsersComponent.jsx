import api from "../../../api";
import { useEffect, useState } from "react";
import { useTheme } from "../../../Context/ThemeContext";
import style from "../../../styles/components/userscomponent.module.css";
import Notification from "../../../Components/Common/NotificationComponent";
import getResponseMessages from "../../../utils/extractResponseMessage";
import UsersPerDivision from "./UsersPerDivisionComponent";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import { Link } from "react-router-dom";

export default function AllUsersComponent({ setUserPage, setUserId }) {
  const [visible, setVisible] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(true);
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
        setLoading(false);
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
          {loading ? (
            <BaseSkeleton height={37} width={200} />
          ) : (
            <div className={style.title}>
              <p>User Management</p>
            </div>
          )}
          {loading ? (
            <BaseSkeleton height={37} width={100} />
          ) : (
            <Link to="/home/users/add">
              <button>New User</button>
            </Link>
          )}
        </div>
        <div className={style.divisions}>
          <UsersPerDivision
            loading={loading}
            usersPerDivision={usersPerDivision}
            setUserPage={setUserPage}
            setUserId={setUserId}
          />
        </div>
      </div>
      <Notification isVisible={visible} response={response} />
    </>
  );
}
