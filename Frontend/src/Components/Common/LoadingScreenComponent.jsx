import ClipLoader from "react-spinners/ClipLoader";
import style from "../../styles/components/loadingscreencomponent.module.css";
import { useTheme } from "../../Context/ThemeContext";

export default function LoadingScreen() {
  const { theme } = useTheme();
  return (
    <div className={`${style.loadingScreenPage} ${!theme && style.dark}`}>
      <div className={style.loaderContainer}>
        <ClipLoader size={100} color={`${!theme ? "#808080" : "#004700"}`} />
        <p>This will take a second...</p>
      </div>
    </div>
  );
}
