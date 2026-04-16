import style from "../../../styles/components/userscomponent.module.css";
import image from "../../../assets/images/default.png";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import { MdShield, MdPreview, MdPerson } from "react-icons/md";

export default function UsersPerDivision({
  loading,
  usersPerDivision,
  setUserPage,
  setUserId,
}) {
  const getRoleIcon = (role) => {
    switch (role) {
      case "ADMINISTRATOR":
        return <MdShield className={style.icon} />;
      case "STANDARD USER":
        return <MdPerson className={style.icon} />;
      case "VIEWER":
        return <MdPreview className={style.icon} />;
      default:
        break;
    }
  };

  return (
    <>
      {usersPerDivision.map(({ division_name: divisionName, users }) => {
        return (
          <div
            key={divisionName}
            className={style.divisionNameAndUsersContainer}
          >
            {loading ? (
              <BaseSkeleton height={40} width={150} />
            ) : (
              <div className={style.divisionName}>
                <p>{divisionName}</p>
              </div>
            )}

            {loading ? (
              <BaseSkeleton height={200} />
            ) : (
              <div className={style.userList}>
                {users.length === 0 ? (
                  <div className={style.noUsers}>
                    <p>No Users</p>
                  </div>
                ) : (
                  users.map(
                    ({
                      id,
                      fullname,
                      username,
                      role,
                      grade_name: gradeName,
                    }) => {
                      return (
                        <div
                          key={id}
                          onClick={() => {
                            setUserId(id);
                            setUserPage("Update User");
                          }}
                          className={style.userInfo}
                        >
                          <div className={style.iconContainer}>
                            {getRoleIcon(role)}
                          </div>
                          <div className={style.profilePicture}>
                            <img
                              src={image}
                              alt="Profile Picture"
                              width={60}
                              height={60}
                            />
                          </div>
                          <div className={style.infoSection}>
                            <div className={style.fullName}>
                              <p>{fullname}</p>
                            </div>
                            <div className={style.username}>
                              <i>
                                <p>@{username}</p>
                              </i>
                            </div>
                            <div className={style.grade}>
                              <p>{gradeName}</p>
                            </div>
                          </div>
                        </div>
                      );
                    },
                  )
                )}
              </div>
            )}
          </div>
        );
      })}
    </>
  );
}
