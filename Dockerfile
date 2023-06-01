FROM public.ecr.aws/artefacts/ros2:humble-fortress-0.4.12

ARG JOB_ID
COPY . /ws/src
WORKDIR /ws

RUN apt update -y && rosdep install --from-paths src --ignore-src -r -y
RUN source /opt/ros/humble/setup.bash --extend && MAKEFLAGS="-j1 -l1" colcon build --symlink-install --executor sequential

WORKDIR /ws/src

CMD source /ws/install/setup.bash && artefacts run $ARTEFACTS_JOB_NAME
