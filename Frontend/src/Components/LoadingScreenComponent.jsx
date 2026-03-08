import ClipLoader from "react-spinners/ClipLoader";
import style from "../styles/components/loadingscreencomponent.module.css";

export default function LoadingScreen() {
  return (
    <div className={style.loadingScreenPage}>
      <div className={style.loaderContainer}>
        <ClipLoader size={100} color="#004700" />
        <p>This will take a second...</p>
      </div>
    </div>
  );
}
