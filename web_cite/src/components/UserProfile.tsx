import React from "react";

class UserProfile extends React.Component<any, any> {

    constructor({props}: {props: any}) {
        super(props);
    }

    render() {
        return (
        <div>
            <h1>User Profile</h1>
            <h2>User name: {name}</h2>
        </div>
        )
    }
}