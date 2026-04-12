import style from "../../../styles/components/userscomponent.module.css";

export default function UsersPerDivision({ usersPerDivision }) {
  return (
    <>
      {usersPerDivision.map(({ division_name: divisionName, users }) => {
        return (
          <div
            key={divisionName}
            className={style.divisionNameAndUsersContainer}
          >
            <div className={style.divisionName}>
              <p>{divisionName}</p>
            </div>
            <div className={style.userList}>
              {users.map(({ fullname, username }) => {
                return (
                  <div className={style.userInfo}>
                    <div className={style.fullName}>
                      <p>{fullname}</p>
                    </div>
                    <div className={style.username}>
                      <p>{username}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </>
  );
}
