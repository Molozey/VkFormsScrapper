import React from 'react';
import fig1 from '../images/QAFigure1.svg';
import fig2 from '../images/QAFigure2.svg';
import fig3 from '../images/QAFigure3.svg';
import fig4 from '../images/QAFigure4.svg';
import '../styles/CardQA.css' ;

interface CardStyle {
    num: number;
}

function Figure(figNum: any, styleNum: any) {
    return <img src={figNum} className={styleNum} alt='Unstyled'/>
}


class CardQA extends React.Component<CardStyle> {
    question?: string;
    answer?: string;
    figNum?: string;
    styleNum?: string


    constructor(props: CardStyle) {
        super(props);
        let style_array = this.condStyle(props.num)
        this.figNum = style_array[0]
        this.styleNum = style_array[1]
    }
     // TODO: add constructor with question and answer

    condStyle(num: number) {
        if (num == 1) {
            return ['fig1', fig1]
        } else if (num == 2) {
            return ['fig2', fig2]
        } else if (num == 3) {
            return ['fig3', fig3]
        } else {
            return ['fig4', fig4]
        }
    }

    // @ts-ignore
    render() {
        // console.log(this.figNum)
        // console.log(this.styleNum)
        return (
        <div className='background'>
            // This is not working
            {/*<Figure figNum={this.figNum} styleNum={this.styleNum}/>*/}
            {/*<img src={this.figNum} className={this.styleNum} alt='Unstyled'/>*/}
            // This is working
            <img src={fig1} className={this.styleNum} alt='Unstyled'/>
        </div>

        )
    }
}

export default CardQA;

