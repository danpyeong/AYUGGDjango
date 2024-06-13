import Nav from "../../nav";
import { Logo } from "./mainStyle/mainStyle";
import Search from "./searchBox";

function Main(){
    return(
        <>
            <Nav></Nav>
            <Logo src={`${process.env.PUBLIC_URL}` + 'assets/images/logo/body-logo.png'} />
            <Search></Search>
        </>
    )
}

export default Main;