import { MdShield, MdPreview, MdPerson } from "react-icons/md";
import style from "../../../styles/components/dashboardcomponent.module.css";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import { useNavigate } from "react-router-dom";

export default function UserInfo({ totalUsersPerRole, loading }) {
  const navigate = useNavigate();

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
      <div
        key={role}
        className={style.userInfoContainer}
        onClick={() => navigate(`/home/users/all`)}
      >
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
