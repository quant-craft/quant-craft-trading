from sqladmin import Admin, ModelView
from app.db.models import Bot, Strategy, TradingBot, Order, Trade, User, Backtesting
from app.db.database import engine


class BotAdmin(ModelView, model=Bot):
    column_list = [Bot.id, Bot.name, Bot.dry_run, Bot.cash]


class StrategyAdmin(ModelView, model=Strategy):
    column_list = [Strategy.id, Strategy.name, Strategy.description]


class TradingBotAdmin(ModelView, model=TradingBot):
    column_list = [TradingBot.id, TradingBot.bot_id, TradingBot.strategy_id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.trading_bot_id, Order.size, Order.status,Order.parent_order_id, Order.trade_id]


class TradeAdmin(ModelView, model=Trade):
    column_list = [Trade.id, Trade.trading_bot_id, Trade.size, Trade.entry_price, Trade.exit_price, Trade.orders]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class BacktestingAdmin(ModelView, model=Backtesting):
    column_list = [
        Backtesting.id,
        Backtesting.strategy_name,
        Backtesting.start_date,
        Backtesting.end_date,
        Backtesting.initial_capital,
        Backtesting.final_equity,
        Backtesting.total_return,
        Backtesting.max_drawdown,
        Backtesting.win_rate,
        Backtesting.total_trades
    ]
    column_labels = {
        Backtesting.id: 'ID',
        Backtesting.strategy_name: 'Strategy',
        Backtesting.start_date: 'Start Date',
        Backtesting.end_date: 'End Date',
        Backtesting.initial_capital: 'Initial Capital',
        Backtesting.final_equity: 'Final Equity',
        Backtesting.total_return: 'Total Return (%)',
        Backtesting.max_drawdown: 'Max Drawdown (%)',
        Backtesting.win_rate: 'Win Rate (%)',
        Backtesting.total_trades: 'Total Trades'
    }
    column_formatters = {
        Backtesting.total_return: lambda m, a: f"{m.total_return:.2f}%",
        Backtesting.max_drawdown: lambda m, a: f"{m.max_drawdown:.2f}%",
        Backtesting.win_rate: lambda m, a: f"{m.win_rate:.2f}%",
    }
    column_default_sort = ('id', True)


def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(BotAdmin)
    admin.add_view(StrategyAdmin)
    admin.add_view(TradingBotAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(TradeAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(BacktestingAdmin)
