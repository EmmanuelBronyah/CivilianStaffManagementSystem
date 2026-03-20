import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";
import { useTheme } from "../context/ThemeContext";

export default function BaseSkeleton(props) {
  const { theme } = useTheme();
  return (
    <Skeleton
      height={"100%"}
      baseColor={theme ? "#5fa65f33" : "#2a2a2a"}
      highlightColor={theme ? "#a8d5a8" : "#3a3a3a"}
      duration={1.3}
      borderRadius={8}
      {...props}
    />
  );
}
