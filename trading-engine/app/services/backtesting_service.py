from sqlalchemy.orm import Session
import pandas as pd
from typing import Union, List
from app.db.models import Backtesting, Strategy
from app.model.backtest.Backtest import Backtest
from app.schemas.backtesting import BacktestingCreate
from app.repositories import backtesting_repository
import json
from app.utils.backtest_encoder import BacktestEncoder
from app.services.strategy_manager import StrategyManager


def run(db: Session, data: Union[str, pd.DataFrame], strategy: Strategy, cash: float, commission: float, start_date: str,
        end_date: str) -> Backtesting:
    if isinstance(data, str):
        data = pd.read_csv(data, index_col=0, parse_dates=True)
    elif not isinstance(data, pd.DataFrame):
        raise ValueError("Data must be either a DataFrame or a path to a CSV file.")

    strategy_class = StrategyManager.get_strategy(strategy.name)

    bt = Backtest(data, strategy_class, cash=cash, commission=commission,
                  hedging=strategy.hedge_mode, exclusive_orders=strategy.exclusive_orders)
    stats = bt.run()

    backtesting_data = BacktestingCreate(
        strategy_id=strategy.id,
        strategy_name=strategy.name,
        start_date=start_date,
        end_date=end_date,
        initial_capital=cash,
        final_equity=float(stats['Equity Final [$]']),
        total_return=float(stats['Return [%]']),
        max_drawdown=float(stats['Max. Drawdown [%]']),
        win_rate=float(stats['Win Rate [%]']),
        profit_factor=float(stats['Profit Factor']),
        total_trades=int(stats['# Trades']),
        trades=json.dumps(stats.get('_trades', []), cls=BacktestEncoder),
        equity_curve=json.dumps(stats.get('_equity_curve', pd.DataFrame()), cls=BacktestEncoder)
    )

    return backtesting_repository.create_backtesting(db, backtesting_data)


def get_backtesting(db: Session, backtesting_id: int) -> Backtesting:
    return backtesting_repository.get_backtesting(db, backtesting_id)


def get_backtestings(db: Session, skip: int = 0, limit: int = 100) -> List[Backtesting]:
    return backtesting_repository.get_backtestings(db, skip, limit)


def delete(db: Session, backtesting_id: int) -> bool:
    return backtesting_repository.delete_backtesting(db, backtesting_id)
