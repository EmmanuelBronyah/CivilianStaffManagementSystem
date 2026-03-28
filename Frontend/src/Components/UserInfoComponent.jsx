import { MdShield, MdPreview, MdPerson } from "react-icons/md";
import style from "../styles/components/dashboardcomponent.module.css";
import BaseSkeleton from "./SkeletonComponent";

export default function UserInfo({ totalUsersPerRole, loading }) {
  if (totalUsersPerRole === null) {
    return (
      <>
        <BaseSkeleton />
        <BaseSkeleton />
        <BaseSkeleton />
      </>
    );
  }

  const getIconAndTitle = (role) => {
    switch (role) {
      case "administrators":
        return [<MdShield className={style.icon} />, <p>Administrators</p>];
      case "standard_users":
        return [<MdPerson className={style.icon} />, <p>Standard Users</p>];
      case "viewers":
        return [<MdPreview className={style.icon} />, <p>Viewers</p>];
    }
  };

  const userInfo = Object.entries(totalUsersPerRole).map(([role, total]) => {
    const [icon, title] = getIconAndTitle(role);
    return loading ? (
      <BaseSkeleton />
    ) : (
      <div className={style.userInfoContainer}>
        <div className={style.userIcon}>{icon}</div>
        <div className={style.totalUsersContainer}>
          <p>{total}</p>
        </div>
        <div className={style.userRoleContainer}>{title}</div>
      </div>
    );
  });

  return <>{userInfo}</>;
}
