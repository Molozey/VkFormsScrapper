import React from 'react';
import fig1 from '../images/QAFigure1.svg';
import fig2 from '../images/QAFigure2.svg';
import fig3 from '../images/QAFigure3.svg';
import fig4 from '../images/QAFigure4.svg';
import '../styles/CardQA.css' ;

interface CardStyle {
    num: number;
    question: string;
    answer: string;
}


class CardQA extends React.Component<CardStyle> {
    question?: string;
    answer?: string;
    figNum?: string;
    styleNum?: string


    constructor(props: CardStyle) {
        super(props);
        let style_array = this.condStyle(props.num)
        this.figNum = style_array[1]
        this.styleNum = style_array[0]
        this.question = props.question
        this.answer = props.answer
    }

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
            <div className='mask'>
                <div className='background'>
                    <p className='question'> {this.question} </p>
                    <p className='answer'> {this.answer} </p>
                </div>
                <img src={this.figNum} className={this.styleNum} alt='Unstyled'/>
            </div>
        )
    }
}

export default CardQA;

