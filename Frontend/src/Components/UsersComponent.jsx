import style from "../styles/components/userscomponent.module.css";
import AddUserInputBoxes from "./AddUserInputBoxesComponent";
import { useTheme } from "../context/ThemeContext";

export default function Users() {
  const { theme } = useTheme();

  return (
    <main
      className={`${style.addUserComponentContainer} ${!theme ? style.dark : ""}`}
    >
      <div className={style.allUsersButtonContainer}>
        <button>All Users</button>
      </div>
      <div className={style.addUserContainer}>
        <div className={style.addUserTitle}>
          <p>Add A New User</p>
        </div>
        <AddUserInputBoxes />
        <div className={style.buttonsContainer}>
          <div className={style.addUserButton}>
            <button>Save</button>
          </div>
          <div className={style.addUserButton}>
            <button>Save & Add Another</button>
          </div>
          <div className={style.discardButton}>
            <button>Discard</button>
          </div>
        </div>
      </div>
    </main>
  );
}
