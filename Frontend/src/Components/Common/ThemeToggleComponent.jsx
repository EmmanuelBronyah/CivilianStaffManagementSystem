import style from "../../styles/components/themetogglecomponent.module.css";
import { MdLightMode, MdDarkMode } from "react-icons/md";
import Switch from "react-switch";
import { useTheme } from "../../context/ThemeContext";

export default function ThemeToggle(props) {
  const { theme, setTheme } = useTheme();

  return (
    <Switch
      className={props.className}
      boxShadow={`0px 0px 2px 3px ${theme ? "#004700" : "#3b3b3b"}`}
      activeBoxShadow={`0px 0px 2px 3px ${theme ? "#004700" : "#3b3b3b"}`}
      onColor="#fff"
      offColor="#6a6a6a"
      onHandleColor="#004700"
      offHandleColor="#6a6a6a"
      checkedIcon={<MdLightMode className={style.lightMode} />}
      uncheckedIcon={<MdDarkMode className={style.darkMode} />}
      checked={theme}
      onChange={(checked) => setTheme(checked)}
    />
  );
}
