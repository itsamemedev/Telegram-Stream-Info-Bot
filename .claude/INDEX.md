# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (153)

```
 10453  GET              /                                                dashboard
 14142  GET              /api/abo/status                                  api_abo_status
 10526  GET              /api/active-recordings                           api_active_recordings
 14213  GET              /api/activity-pulse                              api_activity_pulse
 14020  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20695  GET/POST         /api/audio/config                                api_audio_config
 20725  POST             /api/audio/testtone                              api_audio_testtone
 14086  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14110  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14114  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11980  GET              /api/automation/status                           api_automation_status
 12002  POST             /api/automation/toggle                           api_automation_toggle
 13017  GET              /api/azrael/agents                               api_azrael_agents
 11872  POST             /api/azrael/ask                                  api_azrael_ask
 20893  GET/POST         /api/azrael/context                              api_azrael_context
 12722  GET              /api/azrael/core                                 api_azrael_core
 21027  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21017  GET              /api/azrael/live_status                          api_azrael_live_status
 21035  POST             /api/azrael/live_test                            api_azrael_live_test
 13026  GET              /api/azrael/memories                             api_azrael_memories
 21083  POST             /api/azrael/persona                              api_azrael_persona_set
 21074  GET              /api/azrael/personas                             api_azrael_personas
 21111  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20866  POST             /api/azrael/react                                api_azrael_react
 20902  GET              /api/azrael/reaction                             api_azrael_reaction
 21054  GET              /api/azrael/reactions                            api_azrael_reactions
 21104  GET              /api/azrael/transcript                           api_azrael_transcript
 20989  POST             /api/azrael/tts_test                             api_azrael_tts_test
 20964  GET              /api/azrael/voices                               api_azrael_voices
 21128  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10825  GET              /api/backoff-watch                               api_backoff_watch
 13501  POST             /api/backup/run                                  api_backup_run
 13467  GET              /api/backup/status                               api_backup_status
 13456  POST             /api/backup/system                               api_backup_system
 14052  GET              /api/bandwidth/live                              api_bandwidth_live
 14005  GET              /api/bookmarks                                   api_bookmarks_list
 11088  GET              /api/brain                                       api_brain
 11025  GET              /api/brain/alarms                                api_brain_alarms
 11010  GET              /api/brain/creator                               api_brain_creator
 10987  GET              /api/brain/graph                                 api_brain_graph
 11048  GET              /api/brain/growth                                api_brain_growth
 10003  GET              /api/brain/health                                api_brain_health
 21572  GET              /api/channel/categories                          api_channel_categories
 21578  POST             /api/channel/set                                 api_channel_set
 21425  GET              /api/channels/status                             api_channels_status
 20339  POST             /api/chat/send                                   api_chat_send
 13221  GET              /api/chat/send_status                            api_chat_send_status
 10507  GET              /api/checks                                      api_checks
 20930  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20913  GET              /api/clips                                       api_clips
 20946  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20617  GET              /api/cohost                                      api_cohost
 20629  POST             /api/cohost/config                               api_cohost_config
 14521  GET              /api/community/stats                             api_community_stats
 22212  GET              /api/data/export                                 api_data_export
 20543  GET              /api/debug/threads                               api_debug_threads
 23039  GET              /api/defense/attacks                             api_defense_attacks
 23006  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23024  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22730  GET              /api/defense/overview                            api_defense_overview
 13563  POST             /api/discord/announce                            api_discord_announce
 13291  GET              /api/discord/clips_week                          api_discord_clips_week
 13507  GET              /api/discord/community                           api_discord_community
 13249  GET              /api/discord/invite                              api_discord_invite
 12823  GET              /api/discord/overview                            api_discord_overview
 12909  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14034  GET              /api/events                                      api_events
 13338  GET              /api/events/stream                               api_events_stream
 14047  GET              /api/forecast/storage                            api_forecast_storage
 12018  GET              /api/freeai/status                               api_freeai_status
 12765  GET              /api/health                                      api_health
 14065  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14061  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20666  GET              /api/highlights                                  api_highlights
 20678  POST             /api/highlights/config                           api_highlights_config
 20774  POST             /api/kickmod/config                              api_kickmod_config
 20819  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20833  GET              /api/kickmod/learned                             api_kickmod_learned
 20860  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20840  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21171  POST             /api/kickmod/say                                 api_kickmod_say
 21147  POST             /api/kickmod/start                               api_kickmod_start
 20745  GET              /api/kickmod/status                              api_kickmod_status
 21158  POST             /api/kickmod/stop                                api_kickmod_stop
 10387  POST             /api/login                                       dashboard_login_submit
 14506  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14475  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13186  GET              /api/notify/status                               api_notify_status
 13197  POST             /api/notify/test                                 api_notify_test
 10611  GET              /api/outcomes                                    api_outcomes
 22049  POST             /api/overlay/config                              api_overlay_config
 22036  POST             /api/overlay/event                               api_overlay_event
 21941  GET              /api/overlay/state                               api_overlay_state
 10644  GET              /api/profile/<username>                          api_profile
 14231  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14073  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14196  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14173  GET              /api/proxy/trend                                 api_proxy_trend
 12473  GET              /api/public/stats                                api_public_stats
 10487  GET              /api/pulse                                       api_pulse
 13641  GET              /api/recording-attempts                          api_recording_attempts
 20274  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20252  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20293  POST             /api/restream/<int:rid>/start                    api_restream_start
 20564  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21903  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20228  POST             /api/restream/create                             api_restream_create
 12598  GET              /api/restream/deck                               api_restream_deck
 11954  GET              /api/restream/health                             api_restream_health
 21925  POST             /api/restream/layout                             api_restream_layout
 20201  GET              /api/restream/list                               api_restream_list
 11923  POST             /api/restream/report                             api_restream_report
 20577  POST             /api/restream/start_all                          api_restream_start_all
 20603  POST             /api/restream/stop_all                           api_restream_stop_all
 12129  GET              /api/restream/testpush                           api_testpush_status
 12154  POST             /api/restream/testpush                           api_testpush_run
 14606  GET              /api/restream/verify                             api_restream_verify
 13269  GET              /api/retention/preview                           api_retention_preview
 13278  POST             /api/retention/run                               api_retention_run
 13990  GET              /api/search                                      api_search
 22777  GET              /api/selftest                                    api_selftest
 20310  GET              /api/shield/stats                                api_shield_stats
 10548  GET              /api/storage                                     api_storage
 10555  POST             /api/storage/cleanup                             api_storage_cleanup
 14127  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11893  GET              /api/stream/timeline                             api_stream_timeline
 12897  GET              /api/stream/transcript                           api_stream_transcript
 10579  GET              /api/summary/preview                             api_summary_preview
 13706  GET              /api/system                                      api_system
 14554  GET              /api/system/check_timing                         api_check_timing
 14669  GET              /api/system/config_drift                         api_config_drift
 12933  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13044  GET              /api/system/preflight                            api_system_preflight
 13170  GET              /api/system/preflight_history                    api_system_preflight_history
 13403  GET              /api/system/resilience                           api_system_resilience
 14025  GET              /api/tags                                        api_tags_list
 10521  GET              /api/top                                         api_top
 10880  GET              /api/trend-7d                                    api_trend_7d
 20978  GET              /api/tts/<fn>                                    api_tts_file
 22077  GET              /api/upload_window                               api_upload_window
 10625  GET              /api/userstats                                   api_userstats
 12521  GET              /api/version                                     api_version
 13679  GET              /archive/<int:eid>/download                      archive_download
 13736  GET              /download/<int:recording_id>                     download
 13619  GET              /health                                          health
 20512  GET              /healthz                                         healthz
 10378  GET              /login                                           dashboard_login_page
 10408  GET              /logout                                          dashboard_logout
 10415  GET              /manifest.webmanifest                            pwa_manifest
 12961  GET              /metrics                                         api_prometheus_metrics
 21886  GET              /overlay                                         overlay_page
 10439  GET              /pwa-icon-<variant>.png                          pwa_icon
 10425  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (206)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 23503  /ai                     
 23962  /ask                    
 23594  /assign_role            
 23640  /ban                    
 24294  /botstats               
 24218  /clearwarns             
 24258  /clip                   
 24243  /clipoftheweek          
 24085  /clips                  
 23555  /create_category        
 23524  /create_channel         
 23583  /create_group           
 23566  /create_role            
 23540  /create_voice           
 23876  /daily                  
 23992  /event                  
 24035  /events                 
 24131  /follow                 
 24115  /help                   
 23629  /kick                   
 23858  /leaderboard            
 24071  /livenow                
 24101  /post_test              
 23932  /profile                
 23664  /purge                  
 23844  /rank                   
 24058  /recstatus              
 23605  /remove_role            
 23517  /restream_status        
 23616  /set_channel_perms      
 23809  /setup_community        
 23827  /setup_targets          
 24157  /stats                  
 23429  /status                 
 24453  /streaminfo             
 24350  /sys_report             
 24326  /sys_unpause            
 23651  /timeout                
 24229  /topstreamers           
 23459  /track                  
 23443  /tracklist              
 24146  /unfollow               
 23492  /untrack                
 24179  /warn                   
 24203  /warnings               
```

## Discord-Events (4)

```
 24937  on_member_join
 24899  on_message
 24540  on_raw_reaction_add
 24972  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2494-2495   _abo_key
  2515-2533   _abo_probe_dump
 22319-22329  _active_recorder_sync
 17490-17497  _ad_allowlist
 18617-18623  _agent_for
 22331-22349  _ai_calls_total_sync
 18626-18642  _ai_telemetry
 19124-19142  _alert
 25088-25138  _alert_monitor_loop
 25519-25581  _announce_loop
  3436-3439   _anthropic_key
  3446-3448   _anthropic_model
 10131-10134  _arg_int
  2486-2491   _as_dict
 15350-15355  _audio_cfg
 19278-19300  _audio_tap_cmd
 10299-10310  _auth_cookie
 10266-10295  _auth_guard
  1642-1647   _auto_on
 20177-20195  _auto_restream_loop
 26640-26655  _azrael_broadcast_reply
 26540-26562  _azrael_chat_reply
 26523-26537  _azrael_chat_should_reply
 26568-26570  _azrael_gate_cfg
 18647-18661  _azrael_live_state
 21789-21803  _azrael_overlay_state
 19007-19061  _azrael_proactive_loop
 18466-18522  _azrael_reaction_to_chats
 26573-26580  _azrael_reply_all_chats
 26510-26520  _azrael_self_names
 26608-26637  _azrael_send_to
 18664-18685  _azrael_system
 25257-25260  _backup_active
 25338-25351  _backup_loop
 17378-17379  _badwords_path
 25050-25059  _brain_growth_loop
 10956-10983  _brain_growth_snapshot
  2422-2442   _brain_hint_delay
 10948-10950  _brain_history_for
  6515-6543   _brain_notify
 10925-10946  _brain_record
 10952-10954  _brain_stream_recent
 13317-13334  _browser_push
  6559-6646   _build_daily_summary
  2925-3105   _build_native_cmd
 15698-15885  _build_restream_cmd
  3149-3182   _build_ytdlp_cmd
 22271-22278  _cached_probe
  5337-5364   _can_stop_tracking
  1822-1844   _capture_set_cookies
 14290-14293  _cfg_get
 14296-14298  _cfg_set
 21533-21568  _channel_set_all
 14948-14951  _chat_connected
 14954-14970  _chat_disconnected
  8611-8622   _chat_is_forum
 14990-14992  _chat_sanitize
 14994-15003  _chat_src_ok
 14933-14945  _chat_stat
 14973-14976  _chat_stats_snapshot
  3711-3722   _check_ai_alive_sync
  3725-3737   _check_ai_models_sync
 22280-22293  _check_redis_alive_sync
 22295-22315  _check_redis_version_sync
 11555-11598  _classify_pool_anonymity
 11601-11618  _classify_pool_anonymity_bg
   800-804    _claude_chat_sync_metered
 10160-10167  _client_ip
 25613-25640  _clip_prune
 25643-25653  _clip_recfile_for
 26169-26175  _clip_should_velocity
 25694-25776  _clip_to_discord
  3609-3618   _close_ai_session
 26684-26699  _cohost_broadcast
 26666-26670  _cohost_cfg
 26725-26737  _cohost_fire_highlight
 26673-26681  _cohost_gate
 26702-26722  _cohost_highlight
 25825-25859  _community_events_loop
 10779-10781  _conv_messages
  6923-6966   _cookie_alarm_loop
  1894-1898   _cookie_autorefresh_info
  1799-1803   _cookie_header
 13367-13399  _cpu_load_snapshot
  3919-3931   _create_index_safe
 22532-22638  _crowdsec_status
 22498-22529  _crowdsec_via_lapi
 22363-22381  _cscli_bin
 22387-22400  _cscli_path
  6813-6838   _daily_summary_loop
 22418-22435  _darf_journal_lesen
 25062-25085  _db_maintenance_loop
  6782-6810   _db_vacuum_loop
 17513-17537  _detect_foreign_ad
  1380-1391   _diag_path_owner
 18913-18957  _director_finalize
 19724-19731  _director_for
 18862-18910  _director_mark
 26063-26098  _disc_automod_check
 26036-26042  _disc_state_get
 26045-26052  _disc_state_set
 23081-23094  _discord_guild_filesize_bytes
 23280-23289  _discord_invite
 25997-26033  _discord_live_thread
 19064-19076  _discord_notify
 23181-23206  _discord_ops_alert
 25895-25993  _discord_post_user
 23345-25047  _discord_run_once
 23219-23277  _discord_start
 25584-25590  _discord_stop
 23102-23104  _discord_upload_limit_label
 23097-23099  _discord_upload_limit_mb
  6841-6918   _disk_alarm_loop
 28091-28140  _disk_autoclean
 28143-28156  _disk_guard_loop
 28083-28088  _disk_pct
 15307-15309  _drawtext_chain
 13833-13835  _dump_all_threads
 11480-11544  _enrich_proxies_with_geo
  2039-2083   _ensure_cookie_file_netscape
 23292-23342  _ensure_discord_invite
 25790-25822  _ensure_error_channel
  8670-8673   _ensure_notify_topic
 11725-11762  _ensure_proxy_ready
  8624-8651   _ensure_topic
   658-660    _env_int
   663-665    _env_int_range
 25862-25892  _error_channel_loop
 19108-19121  _event_webhook
 14756-14769  _evolution_loop
  5957-5991   _extract_file_payload
  2171-2173   _extract_urls_from_streamurl_node
 22403-22410  _f2b_sudo_hint
 19144-19146  _faster_whisper_available
 17402-17414  _fetch_ldnoobw_de
 11369-11387  _fetch_proxy_list
 19558-19586  _fetch_tiktok_room_id
   734-737    _ff_cmd
 15470-15475  _find_chromium
  3142-3146   _find_external_recorder
  2176-2178   _find_stream_urls
 14341-14366  _fire_webhooks
  7702-7711   _fork_safe
   815-824    _freeai_chat_sync_metered
 22453-22495  _geo_lookup_ips
  3598-3607   _get_ai_session
  7536-7576   _get_live_info
  2712-2719   _get_resolve_semaphore
  7966-8332   _handle_single_tracking
 27935-27937  _hb
 27940-27957  _hb_while
 15008-15010  _highlight_cfg
 15013-15042  _highlight_observe
 15478-15483  _htmlov_screenshot_cmd
 19302-19312  _httpx_proxy
 14374-14386  _in_quiet_hours
 28970-29001  _install_fast_eventloop
 10026-10080  _install_fast_json
 13838-13854  _install_faulthandler
 20420-20429  _intel_ensure_schema
 20467-20502  _intel_index_loop
 20441-20451  _intel_index_one
 20432-20438  _intel_semantic
  5326-5335   _is_authorized
  7867-7873   _is_dead
  2161-2163   _is_hevc
 22438-22444  _is_private_ip
  1544-1551   _is_process_running
  6545-6556   _is_quiet_hours
  1181-1190   _is_upload_window
 10115-10128  _json_error_handler
  6768-6769   _kick_broadcaster_id
 12055-12074  _kick_channel_live
  6680-6722   _kick_follower_count
  6664-6667   _kick_slug
 12548-12579  _kick_user_token
  3968-3971   _kind_from_filename
 14403-14408  _latest_popularity
 17424-17430  _learned_load
 17421-17422  _learned_path
 17432-17440  _learned_save
 19939-19972  _live_react_loop
 19735-19928  _live_react_worker
 18525-18536  _live_transcript_push
 19930-19937  _live_users
 18960-19004  _living_title_loop
 17381-17389  _load_banned_words_file
  1720-1793   _load_cookies_dict
 25263-25335  _local_backup_scan
 10097-10111  _log_5xx
 15893-15905  _looks_like_codec_err
 15888-15890  _looks_like_source_expired
  7783-7813   _loop_fehler
 13858-13867  _loop_heartbeat
 27905-27932  _loop_lag_monitor
 13870-13938  _loop_watchdog_thread
 18405-18419  _loyalty_add
 18396-18402  _loyalty_get
 18422-18430  _loyalty_top
 14540-14542  _manual_donations_total
  7875-7876   _mark_dead
 12226-12242  _marketing_loop
 26587-26605  _maybe_handle_command
 28242-28266  _maybe_hype_clip
  3886-3909   _migrate_columns
 26864-26875  _mod_is_exempt
 26878-26883  _mod_warn_first
 26886-26889  _mod_warn_text
 14796-14804  _modlog
   934-936    _multistream_targets
  7714-7715   _nc_create_subprocess_exec
  7718-7719   _nc_create_subprocess_shell
 12478-12495  _news_loop
 14834-14836  _normalize_ingest
  2353-2370   _note_check_duration
  8664-8667   _notify_topic_name
 18551-18559  _oracle_memories
 18817-18851  _oracle_memorize
 18562-18575  _oracle_persona
 18544-18548  _oracle_recent_text
 15133-15141  _ov_atomic_write
 15121-15127  _ov_bar
 17337-17349  _ov_clip_text
 15130-15131  _ov_oneline
 21853-21882  _overlay_push
 15424-15467  _overlay_render_size
 14895-14899  _overlay_session_reset
 21805-21808  _overlay_src_ok
 17500-17510  _own_invites
 15419-15421  _parse_size
 22646-22726  _parse_ssh_attacks
  7138-7171   _pause_resume_cmd
  1848-1892   _persist_refreshed_cookies
  1686-1718   _pick_checked_pull_proxy
 10196-10209  _pin_auth_value
 10255-10256  _pin_clear_fail
 10235-10238  _pin_locked
 10241-10252  _pin_note_fail
 10212-10232  _pin_ok
 21695-21697  _piper_available
 21660-21682  _piper_list_voices
 21702-21727  _piper_pick_model
 21739-21786  _piper_say
 21653-21657  _piper_voice_roots
 14303-14338  _post_json_threaded
 15398-15416  _probe_video_size
  1572-1589   _proc_is_recorder
 11467-11478  _proxy_geo_cache_put
 11694-11722  _proxy_pool_refresh_loop
  1652-1683   _proxy_report_recording
 13823-13825  _prune_stall_dumps
 12296-12417  _public_stats
 19079-19105  _push_notify
 10357-10359  _pwa_dir
 11438-11453  _quick_validate_proxy
 14369-14371  _quiet_hours_config
 10322-10355  _rate_guard
 18370-18376  _react_warn
  7622-7661   _reap_proc
  2393-2415   _record_check_outcome
   729-731    _redact_stream_urls
 11621-11691  _refresh_proxy_pool
 21685-21691  _resolve_piper_model
  2187-2277   _resolve_via_html
  2535-2689   _resolve_via_webcast_api_v2
  2752-2814   _resolve_via_ytdlp
 26214-26343  _resolve_youtube_ingest
 20011-20018  _restream_active_platforms
 14880-14891  _restream_active_sources
 19589-19688  _restream_chat_guardian
 15045-15117  _restream_chat_push
 14807-14819  _restream_enabled
 15486-15573  _restream_html_overlay_start
 15576-15589  _restream_html_overlay_stop
  1129-1131   _restream_layout_mode
 14845-14868  _restream_overlay_files
 19976-20008  _restream_platform_state
 20139-20174  _restream_resume_after_restart
 15637-15695  _restream_tts_enqueue_wav
 15360-15392  _restream_tts_feeder
 15357-15358  _restream_tts_fifo_path
 15592-15619  _restream_tts_start
 15621-15635  _restream_tts_stop
 20021-20136  _restream_verify_loop
 25228-25240  _retention_loop
 25187-25225  _retention_scan
  2497-2499   _room_is_abo
  5995-6112   _run_ai_call
 13961-13974  _run_async_from_flask
 22447-22450  _run_priv
 28958-28966  _run_selfcheck_and_exit
 25243-25254  _s3_client
  7902-7953   _safe_send
  4590-4606   _sample_net_throughput
 17391-17399  _save_banned_words_file
  2445-2472   _schedule_next_check
 25141-25184  _scheduler_loop
  3912-3916   _schema_pk
 13978-13983  _scraper_session
 26892-26931  _screen_full
 12781-12818  _sec_headers
  2166-2168   _select_stream_from_data_section
 28771-28955  _selfcheck
  8676-8710   _send_live_notice
  1204-1208   _should_defer_upload
 25656-25691  _shrink_for_discord
 10362-10374  _sicheres_ziel
 28163-28180  _sign_health_check
 28183-28202  _sign_health_loop
  7731-7742   _spawn
  7745-7775   _spawn_from_flask
 22770-22773  _st_befund
 19314-19555  _start_chat_listener
 13941-13958  _start_loop_watchdog
 12441-12469  _stats_loop
 12420-12423  _stats_output_path
 12426-12438  _stats_write
  8404-8420   _storage_cleanup_loop
 28222-28229  _story_for
  3204-3210   _stream_url_expiry
  3219-3225   _stream_url_is_fresh
  3212-3217   _stream_url_ttl
 17464-17471  _streamer_persona_get
 17446-17452  _streamer_personas_load
 17443-17444  _streamer_personas_path
 17454-17462  _streamer_personas_save
 15312-15316  _studio_chain
 25360-25482  _system_backup
 25485-25515  _system_backup_loop
 11390-11429  _test_proxy
 12096-12105  _testpush_cfg
 12108-12125  _testpush_exec
 12077-12093  _testpush_resolve_live
  7878-7899   _tg_sprache_setzen
  8583-8593   _tg_topics_load_into_mem
  8580-8581   _tg_topics_path
  8595-8602   _tg_topics_save
 10170-10178  _token_ok
  8605-8609   _topic_forget
 14389-14400  _tracking_max_duration
  4177-4191   _tracking_remove_cleanup
  4208-4220   _tracking_resume_cleanup
  1438-1461   _try_attach_file_handler
 21729-21737  _tts_cleanup
 12033-12037  _tunnel_effective
 21192-21245  _twitch_channel_status
 26934-27077  _twitch_chat_loop
 26748-26851  _twitch_eventsub_loop
  1227-1240   _upload_queue_add
  1251-1253   _upload_queue_count
  1210-1219   _upload_queue_load
  1200-1202   _upload_queue_path
  1242-1249   _upload_queue_remove
  1221-1225   _upload_queue_save
  1255-1296   _upload_window_loop
  7595-7602   _uptime_s
 14822-14831  _url_host
   709-726    _url_ohne_zugang
   793-797    _usage_record_claude
  7816-7860   _verbindung_verloren
  6725-6756   _viewer_sample_loop
  6772-6779   _viewer_stats
 10259-10262  _wants_html
  7605-7619   _warn_empty_env
 27978-28073  _watchdog_loop
 26489-26497  _wchat_thank_ok
 19148-19178  _whisper_get_model
  7692-7699   _whisper_native_section
 18357-18363  _whisper_pool
 19247-19276  _whisper_segments
 19180-19244  _whisper_transcribe
 15143-15305  _write_restream_overlay
 27105-27184  _youtube_api_chat_loop
 21248-21351  _youtube_api_status
 21354-21421  _youtube_channel_status
 27187-27347  _youtube_chat_loop
 26349-26362  _youtube_restream_autoconfig
 26365-26389  _youtube_restream_autoconfig_inner
 26456-26484  _youtube_send
 21489-21530  _youtube_set_channel
 26392-26426  _yt_access_token
 26429-26444  _yt_live_chat_id
 27098-27102  _yt_oauth_configured
 26452-26453  _yt_sendrate_cfg
 27080-27095  _yt_timeout
  2736-2737   _ytdlp_detect_available
  2739-2750   _ytdlp_note_result
 13828-13830  _zombie_child_count
  7472-7496   about
  4087-4091   add_ai_log_entry
  4004-4007   add_archive_entry
  4703-4718   add_archive_rule
  4379-4413   add_recording
  4152-4169   add_tracking
  6115-6148   ai
  3751-3790   ai_chat
  3824-3834   ai_history_append
  3836-3841   ai_history_clear
  3813-3822   ai_history_load
  3798-3811   ai_rate_limit_check
  6177-6185   aireset
 18688-18707  azrael_chat
 27352-27474  brain_cmd
  3228-3412   build_recording_cmd
  4172-4175   bulk_add_trackings
  6969-7028   bulkadd
  8423-8563   check_all_trackings
  4224-4236   claim_live_transition
 17540-18295  class KickModerator
 15908-17224  class RestreamManager
 11807-11849  classify_proxy_anonymity
  6223-6421   cleanup
  5186-5227   cleanup_old_recordings
  4370-4377   clear_recording
 26101-26166  clip_moment
  4534-4583   compute_storage_forecast
  7091-7135   cookies_cmd
  4143-4149   count_trackings_for_chat
  4074-4085   decide_preferred_recorder
  4014-4017   delete_archive_entry
  4720-4728   delete_archive_rule
  5652-5799   diag
 27586-27647  einnahmen_cmd
  4528-4531   find_recordings_by_fingerprint
  4035-4051   finish_recording_attempt
  4196-4198   get_all_active_trackings
  4102-4105   get_all_checks
  4415-4418   get_all_recordings
  4477-4479   get_all_tags_with_counts
  4505-4508   get_annotations_for_recording
  4009-4012   get_archive_entry
  4498-4501   get_bookmarked_recordings
  1915-2032   get_cookie_health
  4465-4471   get_event_log
  4058-4072   get_last_recording_attempt
  2817-2922   get_live_status
  4986-4989   get_manual_recordings
  4513-4516   get_or_compute_inspect_sync
  5262-5306   get_outcome_breakdown
  4484-4487   get_priority_poll_interval
  4681-4690   get_profile_snapshots
  4053-4056   get_recent_recording_attempts
  4420-4423   get_recording_by_id
  4491-4494   get_recording_note
  3546-3569   get_redis
  4132-4135   get_stats
  5153-5184   get_storage_stats
  4821-4823   get_tiktok_status_distribution
  4238-4247   get_tracking_state
  4193-4194   get_trackings_for_group
  5002-5005   get_trash_recordings
  9331-9994   handle_recording_finished
  3934-3959   init_db
  5076-5130   inspect_stream_url
 21848-21850  is_revenue_platform
  4693-4701   list_archive_rules
  5456-5494   live
  7956-7964   live_check_worker
  3621-3655   llm_chat
  3678-3706   llm_chat_sync
  3663-3675   llm_list_models
  4431-4457   log_event
  1506-1539   log_recording_failure
  7285-7334   logs_cmd
 28270-28761  main
  6151-6174   on_ai_media
  7411-7437   on_ai_reply
  7440-7469   on_azrael_mention
  7501-7531   on_callback
 18710-18814  oracle_handle
  7174-7177   pause_tracking
  5316-5321   profile_keyboard
  7236-7282   quota
  8334-8401   reaper_loop
  4817-4819   record_tiktok_status
  6190-6220   recstatus
  3571-3579   redis_get_json
  3581-3587   redis_set_json
 27650-27660  report_cmd
 11852-11854  report_proxy_result
  2280-2307   resolve_tiktok_live_stream
  4997-5000   restore_recording
  7180-7183   resume_tracking
  4731-4811   run_archive_rules
 27663-27885  run_bot
 13750-13797  run_flask
  4609-4654   sample_bandwidth_for_active
  4660-4679   save_profile_snapshot
  4094-4100   save_tiktok_check
  4362-4368   set_recording_file
  4201-4205   set_tracking_paused
  4992-4995   soft_delete_recording
  8716-9329   split_and_send_video
  5369-5411   start
  4019-4033   start_recording_attempt
  6424-6462   stats
  4967-4984   stop_manual_recording
  7186-7233   stoprec
  6649-6657   summary_cmd
  7337-7408   sysres
  5801-5945   teststream
  5413-5454   tiktok
  7031-7088   topusers
  5531-5588   track
  5496-5528   track_exact
  5602-5650   tracklist
  4833-4965   trigger_manual_recording
  4323-4360   try_acquire_recording_lock
  5008-5067   universal_search
  5590-5600   untrack
 27477-27583  update_cmd
  4523-4526   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
