import {
    createBrowserRouter,
} from "react-router-dom";
import App from "../App";
import Multi from "../page/multi/multiPage";
import SearchPage from "../page/search/searchPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path:"/multi",
    element:<Multi></Multi>
  },
  {
    path:"/search/:gameName/:tagLine",
    element:<SearchPage></SearchPage>
  },

]);

export default router;