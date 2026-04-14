import { useState } from "react";
import AddUsersComponent from "./AddUsersComponent";
import AllUsersComponent from "./AllUsersComponent";
import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import UpdateUser from "./UpdateUserComponent";

export default function Users() {
  const [userPage, setUserPage] = useState("All Users");
  const [userId, setUserId] = useState(null);
  const { theme } = useTheme();

  return (
    <main className={`${style.usersMain} ${!theme ? style.dark : ""}`}>
      {userPage === "All Users" && (
        <AllUsersComponent setUserPage={setUserPage} setUserId={setUserId} />
      )}
      {userPage === "New User" && (
        <AddUsersComponent setUserPage={setUserPage} />
      )}
      {userPage === "Update User" && (
        <UpdateUser
          userPage={userPage}
          setUserPage={setUserPage}
          userId={userId}
        />
      )}
    </main>
  );
}
