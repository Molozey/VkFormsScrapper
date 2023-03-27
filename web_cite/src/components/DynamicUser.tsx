import React from "react";

interface UserProps {
    user_id: number;

}

interface UserContent {
    readonly user_id: number;
    user_name: string;
    user_last_name: string;
    user_age?: string;

}
class DynamicUser extends React.Component<UserProps>{
    userContent: UserContent = {
        user_id: 0,
        user_name: "default",
        user_age: "unknown",
        user_last_name: "default"
    }
    public changeState(json: any) : void {
        console.log(json)
        this.setState({
            userContent: {
                user_id: this.props.user_id,
                user_name: json.user_first_name,
                user_last_name: json.user_sec_name,
                user_age: "default",
            },
            dataIsLoaded: true
        }
        )
    }

    constructor(userID: UserProps) {
        super(userID);
        this.state = {
            userContent: this.userContent,
            dataIsLoaded: false
        }

        let query: string = `http://127.0.0.1:5000/empty1?user_id=${this.props.user_id}`
        fetch(query, {
            method: "GET",
            headers: {
                "Access-Control-Allow-Origin": "127.0.0.1:5000"
            }
        })
            .then((res) => res.json())
            .then(async (json) =>
                    this.changeState(json));
        }



    render() {
        // @ts-ignore
        const {userContent, dataIsLoaded} = this.state;
        if (!dataIsLoaded) return (
            <div>Wait a Little</div>
        )
        return (
            <div className={"userInformation"}>
                <div>User id: {userContent.user_id}</div>
                <div>User name: {userContent.user_name}</div>
                <div>User last name: {userContent.user_last_name}</div>
            </div>
        )
    }
}
export default DynamicUser