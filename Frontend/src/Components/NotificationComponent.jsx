import style from "../styles/components/notificationcomponent.module.css";

export default function Notification(props) {
  return (
    <div
      className={`${style.notificationContainer} ${
        props.isVisible ? style.show : ""
      } ${props.response?.type === "error" ? style.error : ""}`}
    >
      {props.response?.message}
    </div>
  );
}
