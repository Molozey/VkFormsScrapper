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

function buildUser(props: UserProps): UserContent {
    // HERE WE CALL API
    return {
        user_id: props.user_id,
        user_name: "default",
        user_last_name: "NIGGER",
        user_age: "def"
    }
}

class DynamicUser extends React.Component<UserProps>{
    userContent: UserContent

    constructor(userID: UserProps) {
        super(userID);
        this.userContent = buildUser(userID)
    }

    render() {
        return (
            <div className={"userInformation"}>
                <div>User id: {this.userContent.user_id}</div>
                <div>User name: {this.userContent.user_name}</div>
                <div>User last name: {this.userContent.user_last_name}</div>
            </div>
        )
    }
}
export default DynamicUser