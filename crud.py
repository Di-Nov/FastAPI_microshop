import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result

from core.models import (
    db_helper,
    User,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAssociation,
)


async def crete_user(session: AsyncSession, username: str) -> User:
    try:
        user = User(username=username)
        session.add(user)
        await session.commit()
        print("user", user)
        return user
    except Exception as ex:
        print(ex)


async def create_user_profile(
    session,
    user_id: int,
    first_name: str = None,
    last_name: str = None,
    bio: str = None,
):
    try:
        profile: Profile = Profile(
            first_name=first_name, last_name=last_name, bio=bio, user_id=user_id
        )
        session.add(profile)
        await session.commit()
        print("profile ", profile)
        return profile
    except Exception as ex:
        print(f"User with id={user_id} allready exist", ex)


async def create_post(
    session: AsyncSession, user_id: int, title: str | None = None
) -> Post:
    post = Post(user_id=user_id, title=title)
    session.add(post)
    await session.commit()
    print(f"Create post {post}")
    return post


async def get_user_by_username(session, username):
    stmt = select(User).where(User.username == username)

    try:
        result: Result = await session.execute(stmt)
        user: User = result.scalar_one()

        # or

        # user = await session.scalar(stmt)
        print("Found user ", username, user)
        return user
    except Exception as ex:
        print(ex)


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)

    # or

    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    for user in users:
        print(user)
        print(user.profile.first_name)


async def get_users_with_posts(session: AsyncSession):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    # for user in users.unique():  # type: User

    # or

    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        for post in user.posts:
            print(post.title)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(selectinload(User.posts), joinedload(User.profile))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:  # type: User
        print(user, user.profile)
        for post in user.posts:  # type: Post
            print(post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "john")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main_relations(session: AsyncSession):
    await crete_user(session, "Dimon")
    await crete_user(session, "Piero")

    user_dima = await get_user_by_username(session, "Dima")
    user_dimon = await get_user_by_username(session, "Dimon")
    user_piero = await get_user_by_username(session, "Piero")
    await create_user_profile(session=session, user_id=user_dima.id, first_name="Dima")
    await create_user_profile(session=session, user_id=user_dimon.id, first_name="Dima")
    await create_user_profile(session=session, user_id=user_piero.id, first_name="Dima")
    await show_users_with_profiles(session)
    await create_post(
        session=session, title="It is my first post", user_id=user_dima.id
    )


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession, name: str, description: str, price: int
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")
    mouse = await create_product(
        session=session,
        name="Mouse",
        description="Greate gaming mouse",
        price=2_800,
    )
    keyboard = await create_product(
        session=session,
        name="Keyboard",
        description="Greate gaming keyboard",
        price=5_900,
    )
    display = await create_product(
        session=session,
        name="Display",
        description="Greate gaming display",
        price=25_000,
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_one.products.append(mouse)
    order_one.products.append(keyboard)

    order_promo.products.append(keyboard)
    order_promo.products.append(display)
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products))
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_orders_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:  # type: Order
        print(order.id, order.promocode, order.created_at)
        print("products:")
        for product in order.products:  # type: Product
            print("-", product.id, product.name)


async def get_orders_with_products_assoc(session: AsyncSession) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def demo_orders_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    for order in orders:  # type: Order
        print(order.id, order.promocode, order.created_at)
        print("products:")
        for (
            order_products_details
        ) in order.products_details:  # type: OrderProductAssociation
            print(
                "-",
                order_products_details.product.id,
                order_products_details.product.name,
                order_products_details.count,
            )


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session,
        name="cover",
        description="cover for mouse",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )
    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await demo_orders_with_assoc(session)
    # await create_orders_and_products(session)
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_orders_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
