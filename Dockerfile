# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

FROM python:3.7-buster AS production-environment

WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.1.12
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root --no-interaction

FROM production-environment AS notification-image
COPY app ./app
COPY emails ./emails
ENTRYPOINT ["python3", "-m", "app"]

FROM production-environment AS development-environment
RUN poetry install --no-root --no-interaction

FROM development-environment AS alembic-image
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./
ENTRYPOINT ["python3", "-m", "alembic"]
CMD ["upgrade", "head"]
