import { MdShield, MdPreview, MdPerson } from "react-icons/md";
import style from "../styles/components/dashboardcomponent.module.css";

export default function UserInfo({ role, total }) {
  let variables;

  if (role === "administrators") {
    variables = [<MdShield className={style.icon} />, <p>Administrators</p>];
  } else if (role === "standard_users") {
    variables = [<MdPerson className={style.icon} />, <p>Standard Users</p>];
  } else if (role === "viewers") {
    variables = [<MdPreview className={style.icon} />, <p>Viewers</p>];
  }

  const [icon, title] = variables;

  return (
    <div className={style.userInfoContainer}>
      <div className={style.userIcon}>{icon}</div>
      <div className={style.totalUsersContainer}>
        <p>{total}</p>
      </div>
      <div className={style.userRoleContainer}>{title}</div>
    </div>
  );
}
