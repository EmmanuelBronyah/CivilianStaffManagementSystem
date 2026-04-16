import { useState } from "react";
import AddUsersComponent from "./AddUsersComponent";
import AllUsersComponent from "./AllUsersComponent";
import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import UpdateUser from "./UpdateUserComponent";

export default function Users(props) {
  const [userId, setUserId] = useState(null);
  const { theme } = useTheme();

  return (
    <main className={`${style.usersMain} ${!theme ? style.dark : ""}`}>
      {props.userPage === "All Users" && (
        <AllUsersComponent
          setUserPage={props.setUserPage}
          setUserId={setUserId}
        />
      )}
      {props.userPage === "New User" && (
        <AddUsersComponent setUserPage={props.setUserPage} />
      )}
      {props.userPage === "Update User" && (
        <UpdateUser
          userPage={props.userPage}
          setUserPage={props.setUserPage}
          userId={userId}
        />
      )}
    </main>
  );
}
